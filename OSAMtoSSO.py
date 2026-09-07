"""Convert an O-SAM structural analysis model (JSON) into an SSO RDF graph.

The input JSON is parsed and validated through osam.py's Pydantic schema
(StructuralAnalysisModel), then the validated model is walked to build an
rdflib.Graph using exactly the classes and properties SSO.py declares,
which is finally serialized to Turtle.

Usage:
    python OSAMtoSSO.py <input.osam> [-o output.ttl] [--base-uri URI]
                         [--include CATEGORY [CATEGORY ...] | --exclude CATEGORY [CATEGORY ...]]

By default every category of entity is converted. Use --include to convert
only the given categories, or --exclude to convert everything except them
(see CATEGORIES below).
"""

import argparse
import datetime
import json
import pathlib
from typing import Optional
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, XSD

from osam import (
    BeamSection,
    BoundaryCondition as OsamBoundaryCondition,
    DistributedLoad,
    Instance,
    LoadCase,
    Material,
    Object,
    PointLoad,
    ShellSection,
    SolidSection,
    StructuralAnalysisModel,
    SurfaceLoad,
)

# Must match the ontology IRI declared in SSO.py (`ref`).
SSO_NAMESPACE = "https://w3id.org/sso#"

# Default namespace minted for converted instance data.
DEFAULT_BASE_URI = "http://www.upclabmodelsdigitals.org/Models/OSAM/"

# Filterable categories of entities, one per Converter section/loop that can
# be switched off independently via --include/--exclude (see Converter.include
# below). "nodes"/"elements" only take effect when "objects" is also
# included, and "nsets"/"elsets" only take effect when "assembly" is also
# included — excluding the container skips its contents regardless.
CATEGORIES = (
    "units", "objects", "nodes", "elements", "materials", "sections",
    "assembly", "nsets", "elsets", "load_cases", "loads",
    "boundary_conditions",
)


##########################################################
#            Legacy OSAM shape normalization              #
##########################################################
#
# osam.py documents a flat schema (section/load bodies live directly on
# their parent, and cross_section always carries its own "type"
# discriminator). Some real OSAM exports still nest a section's/load's
# type-specific fields under a "section"/"load" wrapper key, and omit the
# cross_section "type" key. This normalizes that legacy shape into what
# osam.py expects, without changing osam.py itself.

_BEAM_PROFILE_TYPES = {
    "RECT", "BOX", "PIPE", "CIRC", "I", "L", "HEX", "TRAPEZOID",
    "GENERAL", "NON LINEAR GENERAL", "ARBITRARY",
}


def _flatten_wrapper(entry: dict, wrapper_key: str) -> dict:
    """Merge a nested wrapper dict's keys onto its parent; parent wins on clash."""
    wrapper = entry.get(wrapper_key)
    if not isinstance(wrapper, dict):
        return entry
    merged = dict(wrapper)
    merged.update({k: v for k, v in entry.items() if k != wrapper_key})
    return merged


def _normalize_section(entry: dict) -> dict:
    entry = _flatten_wrapper(entry, "section")
    if entry.get("section_type") == "BEAM SECTION":
        cross_section = entry.get("cross_section")
        if isinstance(cross_section, dict) and "type" not in cross_section:
            beam_section = entry.get("beam_section")
            if beam_section not in _BEAM_PROFILE_TYPES:
                raise ValueError(
                    f"Section {entry.get('id')!r} ({entry.get('name')!r}): "
                    f"cross_section has no 'type' and beam_section "
                    f"{beam_section!r} is not a recognized profile shape; "
                    "cannot infer the cross-section's type."
                )
            entry = dict(entry)
            entry["cross_section"] = {**cross_section, "type": beam_section}
    return entry


def normalize_osam(data: dict) -> dict:
    """Adapt a raw OSAM JSON payload to the flat shape osam.py expects."""
    data = dict(data)
    if "sections" in data:
        data["sections"] = [_normalize_section(s) for s in data["sections"]]
    if "loads" in data:
        data["loads"] = [_flatten_wrapper(load, "load") for load in data["loads"]]
    return data


##########################################################
#                       Converter                          #
##########################################################


def _local(value) -> str:
    """URI-quote an arbitrary id/name so it's safe as a URI local name."""
    return quote(str(value), safe="")


class Converter:
    """Builds an SSO rdflib.Graph from a validated OSAM StructuralAnalysisModel."""

    def __init__(self, base_uri: str = DEFAULT_BASE_URI, include: Optional[set] = None):
        self.graph = Graph()
        self.add = lambda s, p, o: self.graph.add((s, p, o))
        self.SSO = Namespace(SSO_NAMESPACE)
        self.INST = Namespace(base_uri)
        # Categories of entity to convert; defaults to everything.
        self.include = set(CATEGORIES) if include is None else set(include)

        self.graph.bind("sso", self.SSO)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)
        self.graph.bind("dcterms", DCTERMS)

        # Lookup registries, populated while walking the model, used to
        # resolve cross-references (e.g. an element's section/material)
        # without repeated linear scans over the graph.
        self._materials: dict[str, URIRef] = {}  # material name -> uri
        self._sections: dict[str, URIRef] = {}  # section id -> uri
        self._objects: dict[str, URIRef] = {}  # object id -> uri
        # node/element ids are only unique *within* a mesh, so these are
        # qualified per object id.
        self._object_nodes: dict[str, dict[int, URIRef]] = {}
        self._object_elements: dict[str, dict[int, URIRef]] = {}
        self._instances: dict[str, URIRef] = {}  # instance id -> uri
        # nsets/elsets are scoped per instance.
        self._instance_nsets: dict[str, dict[str, URIRef]] = {}
        self._instance_elsets: dict[str, dict[str, URIRef]] = {}
        self._loadcases: dict[str, URIRef] = {}  # load case name -> uri

    def _uri(self, local) -> URIRef:
        return self.INST[_local(local)]

    # ── Entry point ─────────────────────────────────────────────────────

    def convert(self, model: StructuralAnalysisModel, source: str) -> URIRef:
        SSO, add = self.SSO, self.add

        sam_uri = self._uri(model.id)
        add(sam_uri, RDF.type, SSO.StructuralAnalysisModel)
        add(sam_uri, DCTERMS.identifier, Literal(model.id, datatype=XSD.string))
        add(sam_uri, RDFS.label, Literal(model.name, datatype=XSD.string))
        add(sam_uri, SSO["as_OSAM-json"], Literal(source, datatype=XSD.string))
        add(sam_uri, SSO["format"], Literal("ttl", datatype=XSD.string))
        add(sam_uri, SSO["creation_date"], Literal(
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
            datatype=XSD.dateTime,
        ))

        if "units" in self.include:
            add(sam_uri, SSO.has_units, self._add_units(model.id, model.units))

        # Materials and sections first: elements (added below, via objects)
        # resolve element_material/element_section against these.
        if "materials" in self.include:
            for mat in model.materials:
                add(sam_uri, SSO.has_material, self._add_material(mat))

        if "sections" in self.include:
            for sec in model.sections:
                add(sam_uri, SSO.has_section, self._add_section(sec))

        if "objects" in self.include:
            for obj in model.objects:
                add(sam_uri, SSO.has_object, self._add_object(obj))

        # Assembly/instances next: they resolve referenced_object against
        # the objects above, and their nsets/elsets are needed by bc/loads.
        if "assembly" in self.include:
            add(sam_uri, SSO.has_assembly, self._add_assembly(model.id, model.assembly))

        if "load_cases" in self.include:
            for lc in model.loadCases:
                add(sam_uri, SSO.has_loadCase, self._add_loadcase(lc))

        if "boundary_conditions" in self.include:
            for bc in model.bc:
                add(sam_uri, SSO.has_boundary_condition, self._add_boundary_condition(bc))

        if "loads" in self.include:
            for load in model.loads:
                add(sam_uri, SSO.has_load, self._add_load(load))

        return sam_uri

    # ── Value objects ────────────────────────────────────────────────────

    def _add_units(self, sam_id: str, units) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(f"{sam_id}_Units")
        add(uri, RDF.type, SSO.Units)
        add(uri, SSO.force, Literal(units.force, datatype=XSD.string))
        add(uri, SSO.length, Literal(units.length, datatype=XSD.string))
        add(uri, SSO.temperature, Literal(units.temperature, datatype=XSD.string))
        add(uri, SSO.time, Literal(units.time, datatype=XSD.string))
        add(uri, SSO.mass, Literal(units.mass, datatype=XSD.string))
        return uri

    def _add_vector_xyz(self, uri: URIRef, x: float, y: float, z: float) -> URIRef:
        SSO, add = self.SSO, self.add
        add(uri, RDF.type, SSO.Vector3D)
        add(uri, SSO.X, Literal(float(x), datatype=XSD.float))
        add(uri, SSO.Y, Literal(float(y), datatype=XSD.float))
        add(uri, SSO.Z, Literal(float(z), datatype=XSD.float))
        return uri

    def _add_coordinate_system(self, obj_id: str, cs) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(f"{obj_id}_CoordinateSystem")
        add(uri, RDF.type, SSO.CoordinateSystem)
        add(uri, SSO.xAxis, self._add_vector_xyz(
            self._uri(f"{obj_id}_CoordinateSystem_X"), cs.xAxis.X, cs.xAxis.Y, cs.xAxis.Z))
        add(uri, SSO.yAxis, self._add_vector_xyz(
            self._uri(f"{obj_id}_CoordinateSystem_Y"), cs.yAxis.X, cs.yAxis.Y, cs.yAxis.Z))
        add(uri, SSO.zAxis, self._add_vector_xyz(
            self._uri(f"{obj_id}_CoordinateSystem_Z"), cs.zAxis.X, cs.zAxis.Y, cs.zAxis.Z))
        return uri

    # ── Object / Mesh / Node / Element ──────────────────────────────────

    def _add_object(self, obj: Object) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(obj.id)
        self._objects[obj.id] = uri
        add(uri, RDF.type, SSO.Object)
        add(uri, DCTERMS.identifier, Literal(obj.id, datatype=XSD.string))
        add(uri, RDFS.label, Literal(obj.name, datatype=XSD.string))
        add(uri, SSO.has_coordinate_system, self._add_coordinate_system(obj.id, obj.coordinateSystem))
        add(uri, SSO.has_mesh, self._add_mesh(obj.id, obj.mesh))
        return uri

    def _add_mesh(self, obj_id: str, mesh) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(f"{obj_id}_Mesh")
        add(uri, RDF.type, SSO.Mesh)
        add(uri, SSO.node_count, Literal(mesh.node_count, datatype=XSD.integer))
        add(uri, SSO.el_count, Literal(mesh.el_count, datatype=XSD.integer))

        node_map = self._object_nodes.setdefault(obj_id, {})
        if "nodes" in self.include:
            for node in mesh.nodes:
                node_uri = self._uri(f"{obj_id}_Node_{node.id}")
                node_map[node.id] = node_uri
                add(node_uri, RDF.type, SSO.Node)
                add(node_uri, DCTERMS.identifier, Literal(node.id, datatype=XSD.integer))
                add(node_uri, SSO.X, Literal(node.X, datatype=XSD.float))
                add(node_uri, SSO.Y, Literal(node.Y, datatype=XSD.float))
                add(node_uri, SSO.Z, Literal(node.Z, datatype=XSD.float))
                add(uri, SSO.has_node, node_uri)

        element_map = self._object_elements.setdefault(obj_id, {})
        if "elements" in self.include:
            for elem in mesh.elements:
                elem_uri = self._add_element(obj_id, elem, node_map)
                element_map[elem.id] = elem_uri
                add(uri, SSO.has_element, elem_uri)

        return uri

    _ELEMENT_SUBCLASSES = {"SHELL": "ShellElement", "BEAM": "BeamElement", "SOLID": "SolidElement"}

    def _add_element(self, obj_id: str, elem, node_map: dict) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(f"{obj_id}_Element_{elem.id}")
        add(uri, RDF.type, SSO.Element)
        # The new ontology only has Shell/Beam/Solid element subclasses (no
        # Membrane/Truss); other element types keep the plain sso:Element type.
        subclass = self._ELEMENT_SUBCLASSES.get(elem.type)
        if subclass is not None:
            add(uri, RDF.type, SSO[subclass])

        add(uri, DCTERMS.identifier, Literal(elem.id, datatype=XSD.integer))
        if elem.type:
            add(uri, SSO.element_type, Literal(elem.type, datatype=XSD.string))
        add(uri, SSO.node_count, Literal(elem.node_count, datatype=XSD.integer))
        add(uri, SSO.face_count, Literal(elem.face_count, datatype=XSD.integer))
        if elem.integration:
            add(uri, SSO.integration, Literal(elem.integration, datatype=XSD.string))
        # sso:dofs is non-functional: one triple per active local DOF.
        for dof in elem.dofs:
            add(uri, SSO.dofs, Literal(dof, datatype=XSD.integer))
        # The nodes an element connects to (has_node's domain is open, and
        # explicitly includes Element).
        for node_id in elem.nodes:
            node_uri = node_map.get(node_id)
            if node_uri is not None:
                add(uri, SSO.has_node, node_uri)

        if elem.section:
            section_uri = self._sections.get(elem.section)
            if section_uri is not None:
                add(uri, SSO.element_section, section_uri)
        if elem.material:
            material_uri = self._materials.get(elem.material)
            if material_uri is not None:
                add(uri, SSO.element_material, material_uri)

        return uri

    # ── Assembly / Instance / Nset / Elset ──────────────────────────────

    def _add_assembly(self, sam_id: str, assembly) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(f"{sam_id}_Assembly")
        add(uri, RDF.type, SSO.Assembly)
        add(uri, RDFS.label, Literal(assembly.name, datatype=XSD.string))
        for inst in assembly.instances:
            add(uri, SSO.has_instance, self._add_instance(inst))
        return uri

    def _add_instance(self, inst: Instance) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(inst.id)
        self._instances[inst.id] = uri
        add(uri, RDF.type, SSO.Instance)
        add(uri, DCTERMS.identifier, Literal(inst.id, datatype=XSD.string))
        add(uri, RDFS.label, Literal(inst.name, datatype=XSD.string))

        object_uri = self._objects.get(inst.referenced_object)
        if object_uri is not None:
            add(uri, SSO.referenced_object, object_uri)

        node_map = self._object_nodes.get(inst.referenced_object, {})
        nset_map = self._instance_nsets.setdefault(inst.id, {})
        if "nsets" in self.include:
            for nset in inst.nsets:
                nset_uri = self._uri(f"{inst.id}_Nset_{nset.name}")
                nset_map[nset.name] = nset_uri
                add(nset_uri, RDF.type, SSO.Nset)
                add(nset_uri, RDFS.label, Literal(nset.name, datatype=XSD.string))
                for node_id in nset.nodeIDs:
                    node_uri = node_map.get(node_id)
                    if node_uri is not None:
                        add(nset_uri, SSO.has_node, node_uri)
                add(uri, SSO.has_nset, nset_uri)

        element_map = self._object_elements.get(inst.referenced_object, {})
        elset_map = self._instance_elsets.setdefault(inst.id, {})
        if "elsets" in self.include:
            for elset in inst.elsets:
                elset_uri = self._uri(f"{inst.id}_Elset_{elset.name}")
                elset_map[elset.name] = elset_uri
                add(elset_uri, RDF.type, SSO.Elset)
                add(elset_uri, RDFS.label, Literal(elset.name, datatype=XSD.string))
                for element_id in elset.elementIDs:
                    element_uri = element_map.get(element_id)
                    if element_uri is not None:
                        add(elset_uri, SSO.has_element, element_uri)
                add(uri, SSO.has_elset, elset_uri)

        # OSAM leaves translation/rotation untyped (Any); SSO mirrors that
        # with an untyped (rdfs:Literal) property.
        if inst.translation is not None:
            add(uri, SSO.translation, Literal(str(inst.translation)))
        if inst.rotation is not None:
            add(uri, SSO.rotation, Literal(str(inst.rotation)))

        return uri

    # ── Material ─────────────────────────────────────────────────────────

    def _add_material(self, mat: Material) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(mat.name)
        self._materials[mat.name] = uri
        add(uri, RDF.type, SSO.Material)
        add(uri, RDFS.label, Literal(mat.name, datatype=XSD.string))
        if mat.category:
            add(uri, SSO.material_category, Literal(mat.category, datatype=XSD.string))
        if mat.type:
            add(uri, SSO.material_type, Literal(mat.type, datatype=XSD.string))
        add(uri, SSO.mass_density, Literal(mat.mass_density, datatype=XSD.float))

        elastic_uri = self._uri(f"{mat.name}_ElasticBehaviour")
        add(elastic_uri, RDF.type, SSO.ElasticBehaviour)
        add(elastic_uri, SSO.behaviour_type, Literal(mat.elastic.behaviour_type, datatype=XSD.string))
        if mat.elastic.parameters is not None:
            add(elastic_uri, SSO.E, Literal(mat.elastic.parameters.E, datatype=XSD.float))
            add(elastic_uri, SSO.poisson_ratio, Literal(mat.elastic.parameters.v, datatype=XSD.float))
        add(uri, SSO.has_elastic_behaviour, elastic_uri)

        if mat.plastic is not None:
            plastic_uri = self._uri(f"{mat.name}_PlasticBehaviour")
            add(plastic_uri, RDF.type, SSO.PlasticBehaviour)
            if mat.plastic.yield_stress is not None:
                add(plastic_uri, SSO.yield_stress, Literal(mat.plastic.yield_stress, datatype=XSD.float))
            if mat.plastic.plastic_strain is not None:
                add(plastic_uri, SSO.plastic_strain, Literal(mat.plastic.plastic_strain, datatype=XSD.float))
            # mat.plastic.functions isn't modeled in SSO, same as
            # ArbitraryProfile's polygon points.
            add(uri, SSO.has_plastic_behaviour, plastic_uri)

        return uri

    # ── Section / Cross-section profile ─────────────────────────────────

    def _add_section(self, sec) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(sec.id)
        self._sections[sec.id] = uri
        add(uri, DCTERMS.identifier, Literal(sec.id, datatype=XSD.string))
        add(uri, RDFS.label, Literal(sec.name, datatype=XSD.string))

        if sec.material:
            material_uri = self._materials.get(sec.material)
            if material_uri is not None:
                add(uri, SSO.section_material, material_uri)

        if isinstance(sec, BeamSection):
            add(uri, RDF.type, SSO.BeamSection)
            add(uri, SSO.beam_section, Literal(sec.beam_section, datatype=XSD.string))
            ox, oy, oz = (list(sec.orientation) + [0.0, 0.0, 0.0])[:3]
            add(uri, SSO.orientation, self._add_vector_xyz(self._uri(f"{sec.id}_Orientation"), ox, oy, oz))
            add(uri, SSO.has_cross_section, self._add_cross_section(sec.id, sec.cross_section))
        elif isinstance(sec, ShellSection):
            add(uri, RDF.type, SSO.ShellSection)
            add(uri, SSO.thickness, Literal(sec.thickness, datatype=XSD.float))
        elif isinstance(sec, SolidSection):
            add(uri, RDF.type, SSO.SolidSection)

        return uri

    def _add_cross_section(self, sec_id: str, profile) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(f"{sec_id}_CrossSection")
        ptype = profile.type

        if ptype == "RECT":
            add(uri, RDF.type, SSO.RectProfile)
            add(uri, SSO.a, Literal(profile.a, datatype=XSD.float))
            add(uri, SSO.b, Literal(profile.b, datatype=XSD.float))
        elif ptype == "BOX":
            add(uri, RDF.type, SSO.BoxProfile)
            add(uri, SSO.a, Literal(profile.a, datatype=XSD.float))
            add(uri, SSO.b, Literal(profile.b, datatype=XSD.float))
            add(uri, SSO.t1, Literal(profile.t1, datatype=XSD.float))
            add(uri, SSO.t2, Literal(profile.t2, datatype=XSD.float))
            add(uri, SSO.t3, Literal(profile.t3, datatype=XSD.float))
            add(uri, SSO.t4, Literal(profile.t4, datatype=XSD.float))
        elif ptype == "PIPE":
            add(uri, RDF.type, SSO.PipeProfile)
            add(uri, SSO.r, Literal(profile.r, datatype=XSD.float))
            add(uri, SSO.t, Literal(profile.t, datatype=XSD.float))
        elif ptype == "CIRC":
            add(uri, RDF.type, SSO.CircProfile)
            add(uri, SSO.radius, Literal(profile.radius, datatype=XSD.float))
        elif ptype == "I":
            add(uri, RDF.type, SSO.IProfile)
            add(uri, SSO.h, Literal(profile.h, datatype=XSD.float))
            add(uri, SSO.b1, Literal(profile.b1, datatype=XSD.float))
            add(uri, SSO.b2, Literal(profile.b2, datatype=XSD.float))
            add(uri, SSO.t1, Literal(profile.t1, datatype=XSD.float))
            add(uri, SSO.t2, Literal(profile.t2, datatype=XSD.float))
            add(uri, SSO.t3, Literal(profile.t3, datatype=XSD.float))
            if profile.l is not None:
                add(uri, SSO.l, Literal(profile.l, datatype=XSD.float))
        elif ptype == "L":
            add(uri, RDF.type, SSO.LProfile)
            add(uri, SSO.a, Literal(profile.a, datatype=XSD.float))
            add(uri, SSO.b, Literal(profile.b, datatype=XSD.float))
            add(uri, SSO.t1, Literal(profile.t1, datatype=XSD.float))
            add(uri, SSO.t2, Literal(profile.t2, datatype=XSD.float))
        elif ptype == "HEX":
            add(uri, RDF.type, SSO.HexProfile)
            add(uri, SSO.circ_r, Literal(profile.circ_r, datatype=XSD.float))
            add(uri, SSO.t, Literal(profile.t, datatype=XSD.float))
        elif ptype == "TRAPEZOID":
            add(uri, RDF.type, SSO.TrapezoidProfile)
            add(uri, SSO.a, Literal(profile.a, datatype=XSD.float))
            add(uri, SSO.b, Literal(profile.b, datatype=XSD.float))
            add(uri, SSO.c, Literal(profile.c, datatype=XSD.float))
            add(uri, SSO.d, Literal(profile.d, datatype=XSD.float))
        elif ptype in ("GENERAL", "NON LINEAR GENERAL"):
            # Both OSAM types carry the same properties; one SSO class covers both.
            add(uri, RDF.type, SSO.GeneralProfile)
            add(uri, SSO.A, Literal(profile.A, datatype=XSD.float))
            add(uri, SSO.I11, Literal(profile.I11, datatype=XSD.float))
            add(uri, SSO.I12, Literal(profile.I12, datatype=XSD.float))
            add(uri, SSO.I22, Literal(profile.I22, datatype=XSD.float))
            add(uri, SSO.J, Literal(profile.J, datatype=XSD.float))
        elif ptype == "ARBITRARY":
            add(uri, RDF.type, SSO.ArbitraryProfile)
            # edge_points/void_points polygon geometry isn't modeled in SSO.
        else:
            raise ValueError(f"Unrecognized cross-section profile type: {ptype!r}")

        return uri

    # ── Load case / Boundary condition / Load ───────────────────────────

    def _add_loadcase(self, lc: LoadCase) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(lc.id)
        self._loadcases[lc.name] = uri
        add(uri, RDF.type, SSO.LoadCase)
        add(uri, DCTERMS.identifier, Literal(lc.id, datatype=XSD.string))
        add(uri, RDFS.label, Literal(lc.name, datatype=XSD.string))
        if lc.type:
            add(uri, SSO.loadCase_type, Literal(lc.type, datatype=XSD.string))
        sx, sy, sz = (list(lc.selfWeight) + [0.0, 0.0, 0.0])[:3]
        add(uri, SSO.selfWeight, self._add_vector_xyz(self._uri(f"{lc.id}_SelfWeight"), sx, sy, sz))
        return uri

    def _resolve_nset(self, instance_ids: Optional[list], name: str) -> Optional[URIRef]:
        for inst_id in instance_ids or []:
            nset_uri = self._instance_nsets.get(inst_id, {}).get(name)
            if nset_uri is not None:
                return nset_uri
        return None

    def _resolve_elset(self, instance_ids: Optional[list], name: str) -> Optional[URIRef]:
        for inst_id in instance_ids or []:
            elset_uri = self._instance_elsets.get(inst_id, {}).get(name)
            if elset_uri is not None:
                return elset_uri
        return None

    def _add_boundary_condition(self, bc: OsamBoundaryCondition) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(bc.id)
        add(uri, RDF.type, SSO.BoundaryCondition)
        add(uri, DCTERMS.identifier, Literal(bc.id, datatype=XSD.string))
        if bc.type:
            add(uri, SSO.bc_type, Literal(bc.type, datatype=XSD.string))

        for inst_id in bc.instances or []:
            inst_uri = self._instances.get(inst_id)
            if inst_uri is not None:
                add(uri, SSO.applied_to, inst_uri)

        # sso:nset is functional (at most one value), while an OSAM bc could
        # in principle name-match sets on several applied instances — take
        # the first match as a best-effort resolution.
        nset_uri = self._resolve_nset(bc.instances, bc.nset)
        if nset_uri is not None:
            add(uri, SSO.nset, nset_uri)

        # Each ux/uy/uz/rx/ry/rz is [restrained: bool, prescribed: float],
        # split per SSO.py into a restrained flag and an optional prescribed value.
        for axis, values in (
            ("ux", bc.ux), ("uy", bc.uy), ("uz", bc.uz),
            ("rx", bc.rx), ("ry", bc.ry), ("rz", bc.rz),
        ):
            if len(values) >= 1:
                add(uri, SSO[f"restrained_{axis}"], Literal(bool(values[0]), datatype=XSD.boolean))
            if len(values) >= 2:
                add(uri, SSO[f"prescribed_{axis}"], Literal(float(values[1]), datatype=XSD.float))

        return uri

    def _add_load(self, load) -> URIRef:
        SSO, add = self.SSO, self.add
        uri = self._uri(load.id)
        add(uri, DCTERMS.identifier, Literal(load.id, datatype=XSD.string))

        loadcase_uri = self._loadcases.get(load.caseName)
        if loadcase_uri is not None:
            add(uri, SSO.in_loadCase, loadcase_uri)

        for inst_id in load.instances or []:
            inst_uri = self._instances.get(inst_id)
            if inst_uri is not None:
                add(uri, SSO.applied_to, inst_uri)

        if isinstance(load, PointLoad):
            add(uri, RDF.type, SSO.PointLoad)
            nset_uri = self._resolve_nset(load.instances, load.nset)
            if nset_uri is not None:
                add(uri, SSO.nset, nset_uri)
            add(uri, SSO.dof, Literal(load.dof, datatype=XSD.integer))
            add(uri, SSO.v, Literal(load.v, datatype=XSD.float))
        elif isinstance(load, DistributedLoad):
            add(uri, RDF.type, SSO.DistributedLoad)
            elset_uri = self._resolve_elset(load.instances, load.elset)
            if elset_uri is not None:
                add(uri, SSO.elset, elset_uri)
            add(uri, SSO.dir, Literal(load.dir, datatype=XSD.string))
            add(uri, SSO.v1, Literal(load.v1, datatype=XSD.float))
            add(uri, SSO.v2, Literal(load.v2, datatype=XSD.float))
            add(uri, SSO.x1, Literal(load.x1, datatype=XSD.float))
            add(uri, SSO.x2, Literal(load.x2, datatype=XSD.float))
        elif isinstance(load, SurfaceLoad):
            add(uri, RDF.type, SSO.SurfaceLoad)
            elset_uri = self._resolve_elset(load.instances, load.elset)
            if elset_uri is not None:
                add(uri, SSO.elset, elset_uri)
            add(uri, SSO.v, Literal(load.v, datatype=XSD.float))
            add(uri, SSO.xdir, Literal(load.xdir, datatype=XSD.float))
            add(uri, SSO.ydir, Literal(load.ydir, datatype=XSD.float))
            add(uri, SSO.zdir, Literal(load.zdir, datatype=XSD.float))
        else:
            add(uri, RDF.type, SSO.Load)

        return uri


##########################################################
#                          CLI                             #
##########################################################


def convert_file(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    base_uri: str,
    include: Optional[set] = None,
) -> Graph:
    with open(input_path, "r", encoding="utf-8") as fp:
        raw = json.load(fp)
    raw = normalize_osam(raw)
    model = StructuralAnalysisModel.model_validate(raw)

    converter = Converter(base_uri=base_uri, include=include)
    converter.convert(model, source=str(input_path))
    converter.graph.serialize(destination=str(output_path), format="turtle")
    return converter.graph


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Convert an O-SAM structural analysis model (JSON) into an SSO RDF graph (Turtle).",
    )
    parser.add_argument("input", type=pathlib.Path, help="Path to the input O-SAM JSON file.")
    parser.add_argument(
        "-o", "--output", type=pathlib.Path, default=None,
        help="Path to the output Turtle file (default: <input>.ttl next to the input file).",
    )
    parser.add_argument(
        "--base-uri", default=DEFAULT_BASE_URI,
        help=f"Namespace URI minted for converted instance data (default: {DEFAULT_BASE_URI}).",
    )
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument(
        "--include", nargs="+", choices=CATEGORIES, metavar="CATEGORY",
        help="Only convert these categories (default: all). 'nodes'/'elements' only take "
             "effect if 'objects' is also included; 'nsets'/'elsets' only take effect if "
             "'assembly' is also included. Choices: " + ", ".join(CATEGORIES),
    )
    filter_group.add_argument(
        "--exclude", nargs="+", choices=CATEGORIES, metavar="CATEGORY",
        help="Convert every category except these. Choices: " + ", ".join(CATEGORIES),
    )
    args = parser.parse_args(argv)

    if args.include:
        include = set(args.include)
    elif args.exclude:
        include = set(CATEGORIES) - set(args.exclude)
    else:
        include = None

    output_path = args.output if args.output is not None else args.input.with_suffix(".ttl")
    convert_file(args.input, output_path, args.base_uri, include=include)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
