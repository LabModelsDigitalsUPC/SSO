from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, VANN, DCTERMS, XSD, PROV

ref =  URIRef("https://w3id.org/sso#")
save_path =  'sso'

# Instantiate  empty  graph for the ontology
g  = Graph()

# Create a namespaces
SSO = Namespace(ref)
CC = Namespace('http://creativecommons.org/ns#')
BEO = Namespace('https://w3id.org/beo#')
BOT = Namespace('https://w3id.org/bot#')
BROT = Namespace('https://w3id.org/brot/0.21')

# Bind your custom prefix
g.bind("sso", SSO)
g.bind('rdf',RDF)
g.bind('rdfs',RDFS)
g.bind('owl', OWL)
g.bind('xsd', XSD)
g.bind('cc', CC)
g.bind('beo', BEO)
g.bind('bot', BOT)
g.bind('brot', BROT)
g.bind('prov', PROV)
g.bind('dcterms', DCTERMS)
g.bind('vann', VANN)

#add ontology header triples
g.add((ref, RDF.type, OWL.Ontology))
g.add((ref, DCTERMS.creator, Literal('Héctor Posada Cárcamo (hector.posada@upc.edu)')))
g.add((ref, DCTERMS.creator, Literal('Carlos Ramonell Cazador (carlos.ramonell@upc.edu)')))
g.add((ref, DCTERMS.creator, Literal('Rolando Chacón Flores (rolando.chacon@upc.edu)')))
g.add((ref, DCTERMS.date, Literal('2026/04/04')))
g.add((ref, DCTERMS.title, Literal('SSO')))
g.add((ref, DCTERMS.description, Literal("Ontology containing the description of structural simulation models (OSAM)")))
g.add((ref, DCTERMS.format, Literal('ttl')))
g.add((ref, DCTERMS.identifier, Literal('SSO')))
g.add((ref, DCTERMS.language, Literal('en')))
g.add((ref, VANN.preferredNamespacePrefix, Literal('sso')))
g.add((ref, VANN.preferredNamespaceUri, Literal(ref)))
g.add((ref, CC.license, Literal('http://creativecommons.org/licenses/by/3.0/')))

# ── WIDOCO metadata ────────────────────────────────────────────────────────
g.add((ref, RDFS.label, Literal("SSO — Structural Simulation Ontology", lang="en")))
g.add((ref, RDFS.comment, Literal(
    "An ontology for representing structural analysis (simulation) models and "
    "linking their finite elements to the built elements they idealize, within "
    "the O-SAM ecosystem.", lang="en")))
g.add((ref, DCTERMS.description, Literal(
    "SSO describes structural analysis models, their materials and constitutive "
    "behaviours, and the calibration events that update those behaviours against "
    "measured data.", lang="en")))
g.add((ref, OWL.versionInfo, Literal("0.1.0")))
g.add((ref, DCTERMS.publisher, Literal('Universitat Politècnica de Catalunya')))
# TODO: add ORCID-based dcterms:creator once available, e.g.:
# g.add((ref, DCTERMS.creator, URIRef("https://orcid.org/XXXX-XXXX-XXXX-XXXX")))
# TODO: confirm dcterms:license (cc:license is already asserted above)
# g.add((ref, DCTERMS.license, URIRef("http://creativecommons.org/licenses/by/3.0/")))


##########################################################
#                       classes                          #
##########################################################

g.add((SSO['StructuralAnalysisModel'], RDF.type, OWL.Class))
g.add((SSO['StructuralAnalysisModel'], RDFS.label, Literal("Structural Analysis Model", lang="en")))
g.add((SSO['StructuralAnalysisModel'], RDFS.comment, Literal(
    "A complete structural analysis (simulation) model: it composes a unit "
    "system, one or more structural Objects, an Assembly of their Instances, "
    "and collections of Materials, Sections, Load Cases, Loads, and Boundary "
    "Conditions.", lang="en")))

g.add((SSO['Object'], RDF.type, OWL.Class))
g.add((SSO['Object'], RDFS.label, Literal("Structural Object", lang="en")))
g.add((SSO['Object'], RDFS.comment, Literal(
    "A structural component (e.g. a beam, shell, or solid assembly) defined "
    "in its own local coordinate system: its Mesh of Nodes and Elements, "
    "referencing Sections and Materials. An Object is defined once and "
    "positioned in the model via one or more Instances.", lang="en")))

g.add((SSO['Assembly'], RDF.type, OWL.Class))
g.add((SSO['Assembly'], RDFS.label, Literal("Assembly", lang="en")))
g.add((SSO['Assembly'], RDFS.comment, Literal(
    "The collection of Instances that, together, position the model's "
    "Objects in the global coordinate system — the assembled structural "
    "model on which Sets, Loads, and Boundary Conditions are defined.", lang="en")))

g.add((SSO['Instance'], RDF.type, OWL.Class))
g.add((SSO['Instance'], RDFS.label, Literal("Instance", lang="en")))
g.add((SSO['Instance'], RDFS.comment, Literal(
    "A placement of a structural Object within the Assembly: references the "
    "Object and applies the spatial transformation between the Object's "
    "local coordinate system and the model's global coordinate system. "
    "Multiple Instances may reference the same Object to replicate an "
    "identical mesh without duplicating its data, and carry their own "
    "Node/Element Sets for scoping loads and boundary conditions.", lang="en")))

g.add((SSO['Material'], RDF.type, OWL.Class))
g.add((SSO['Material'], RDFS.label, Literal("Material", lang="en")))
g.add((SSO['Material'], RDFS.comment, Literal(
    "A structural material, assigned to elements via a Section, whose "
    "constitutive behaviour is decomposed into a required Elastic Behaviour "
    "and an optional Plastic Behaviour, alongside its density.", lang="en")))

g.add((SSO['Section'], RDF.type, OWL.Class))
g.add((SSO['Section'], RDFS.label, Literal("Section", lang="en")))
g.add((SSO['Section'], RDFS.comment, Literal(
    "A structural section that assigns geometric and material properties to "
    "the elements referencing it; an abstract type with three concrete "
    "kinds — Beam, Shell, and Solid Section.", lang="en")))

g.add((SSO['Mesh'], RDF.type, OWL.Class))
g.add((SSO['Mesh'], RDFS.label, Literal("Mesh", lang="en")))
g.add((SSO['Mesh'], RDFS.comment, Literal(
    "The finite element discretization of an Object: its nodes and elements.", lang="en")))

g.add((SSO['Element'], RDF.type, OWL.Class))
g.add((SSO['Element'], RDFS.label, Literal("Finite Element", lang="en")))
g.add((SSO['Element'], RDFS.comment, Literal(
    "A discretized finite element in a structural mesh, the basic unit solved "
    "by the analysis (e.g. a solid, shell, or beam element).", lang="en")))

g.add((SSO['SolidElement'], RDF.type, OWL.Class))
g.add((SSO['SolidElement'], RDFS.subClassOf, SSO.Element))
g.add((SSO['SolidElement'], RDFS.label, Literal("Solid Element", lang="en")))
g.add((SSO['SolidElement'], RDFS.comment, Literal(
    "A finite element with a full 3D solid formulation (e.g. a continuum "
    "brick/tetrahedron element).", lang="en")))

g.add((SSO['ShellElement'], RDF.type, OWL.Class))
g.add((SSO['ShellElement'], RDFS.subClassOf, SSO.Element))
g.add((SSO['ShellElement'], RDFS.label, Literal("Shell Element", lang="en")))
g.add((SSO['ShellElement'], RDFS.comment, Literal(
    "A finite element idealizing a thin plate/shell structural member, such as "
    "a slab or wall.", lang="en")))

g.add((SSO['BeamElement'], RDF.type, OWL.Class))
g.add((SSO['BeamElement'], RDFS.subClassOf, SSO.Element))
g.add((SSO['BeamElement'], RDFS.label, Literal("Beam Element", lang="en")))
g.add((SSO['BeamElement'], RDFS.comment, Literal(
    "A finite element idealizing a slender linear structural member, such as a "
    "beam or column, via its cross-section.", lang="en")))

g.add((SSO['LoadCase'], RDF.type, OWL.Class))
g.add((SSO['LoadCase'], RDFS.label, Literal("Load Case", lang="en")))
g.add((SSO['LoadCase'], RDFS.comment, Literal(
    "A named grouping of loads applied together in one analysis case, "
    "optionally including a self-weight contribution.", lang="en")))

g.add((SSO['Load'], RDF.type, OWL.Class))
g.add((SSO['Load'], RDFS.label, Literal("Load", lang="en")))
g.add((SSO['Load'], RDFS.comment, Literal(
    "An action applied to the structure within a Load Case — a point, "
    "distributed, or surface load.", lang="en")))

g.add((SSO['BoundaryCondition'], RDF.type, OWL.Class))
g.add((SSO['BoundaryCondition'], RDFS.label, Literal("Boundary Condition", lang="en")))
g.add((SSO['BoundaryCondition'], RDFS.comment, Literal(
    "A restraint or prescribed displacement applied to a node set, specified "
    "per degree of freedom (ux, uy, uz, rx, ry, rz).", lang="en")))

# ── Value objects ────────────────────────────────────────────────────────────

g.add((SSO['Units'], RDF.type, OWL.Class))
g.add((SSO['Units'], RDFS.label, Literal("Units", lang="en")))
g.add((SSO['Units'], RDFS.comment, Literal(
    "The unit system (force, length, temperature, time, mass) in which a "
    "Structural Analysis Model's values are expressed.", lang="en")))

g.add((SSO['Vector3D'], RDF.type, OWL.Class))
g.add((SSO['Vector3D'], RDFS.label, Literal("3D Vector", lang="en")))
g.add((SSO['Vector3D'], RDFS.comment, Literal(
    "A three-component (X, Y, Z) vector, used for coordinate axes, beam "
    "orientation, and self-weight direction.", lang="en")))

g.add((SSO['CoordinateSystem'], RDF.type, OWL.Class))
g.add((SSO['CoordinateSystem'], RDFS.label, Literal("Coordinate System", lang="en")))
g.add((SSO['CoordinateSystem'], RDFS.comment, Literal(
    "A local coordinate system defined by its X, Y, and Z axis vectors.", lang="en")))

g.add((SSO['Node'], RDF.type, OWL.Class))
g.add((SSO['Node'], RDFS.label, Literal("Node", lang="en")))
g.add((SSO['Node'], RDFS.comment, Literal(
    "A meshed point in space, identified by its coordinates, that finite "
    "elements connect to.", lang="en")))

# ── Sets ─────────────────────────────────────────────────────────────────────

g.add((SSO['Nset'], RDF.type, OWL.Class))
g.add((SSO['Nset'], RDFS.label, Literal("Node Set", lang="en")))
g.add((SSO['Nset'], RDFS.comment, Literal(
    "A named group of nodes, defined on an assembled Instance, used to scope "
    "loads and boundary conditions to a specific part of the model.", lang="en")))

g.add((SSO['Elset'], RDF.type, OWL.Class))
g.add((SSO['Elset'], RDFS.label, Literal("Element Set", lang="en")))
g.add((SSO['Elset'], RDFS.comment, Literal(
    "A named group of elements, defined on an assembled Instance, used to "
    "scope distributed and surface loads to a specific part of the model.", lang="en")))

# ── Material behaviour ────────────────────────────────────────────────────────

g.add((SSO['ElasticBehaviour'], RDF.type, OWL.Class))
g.add((SSO['ElasticBehaviour'], RDFS.label, Literal("Elastic Behaviour", lang="en")))
g.add((SSO['ElasticBehaviour'], RDFS.comment, Literal(
    "The linear-elastic constitutive response of a material, defined by its "
    "behaviour type (isotropic, anisotropic, or orthotropic) and elastic "
    "parameters (Young's modulus, Poisson's ratio).", lang="en")))

g.add((SSO['PlasticBehaviour'], RDF.type, OWL.Class))
g.add((SSO['PlasticBehaviour'], RDFS.label, Literal("Plastic Behaviour", lang="en")))
g.add((SSO['PlasticBehaviour'], RDFS.comment, Literal(
    "The plastic (post-yield) constitutive response of a material, defined by "
    "its yield stress and plastic strain.", lang="en")))

# ── Section subtypes ──────────────────────────────────────────────────────────

g.add((SSO['BeamSection'], RDF.type, OWL.Class))
g.add((SSO['BeamSection'], RDFS.subClassOf, SSO.Section))
g.add((SSO['BeamSection'], RDFS.label, Literal("Beam Section", lang="en")))
g.add((SSO['BeamSection'], RDFS.comment, Literal(
    "A section assigning a named beam profile and orientation to beam "
    "elements, carrying exactly one typed Cross-Section Profile for its "
    "geometry.", lang="en")))

g.add((SSO['ShellSection'], RDF.type, OWL.Class))
g.add((SSO['ShellSection'], RDFS.subClassOf, SSO.Section))
g.add((SSO['ShellSection'], RDFS.label, Literal("Shell Section", lang="en")))
g.add((SSO['ShellSection'], RDFS.comment, Literal(
    "A section assigning a single thickness to shell elements, used for "
    "plate/shell structural members like slabs and walls.", lang="en")))

g.add((SSO['SolidSection'], RDF.type, OWL.Class))
g.add((SSO['SolidSection'], RDFS.subClassOf, SSO.Section))
g.add((SSO['SolidSection'], RDFS.label, Literal("Solid Section", lang="en")))
g.add((SSO['SolidSection'], RDFS.comment, Literal(
    "A section for solid elements, whose geometry comes entirely from the mesh "
    "rather than parametric properties.", lang="en")))

# ── Cross-section profiles ────────────────────────────────────────────────────

g.add((SSO['CrossSectionProfile'], RDF.type, OWL.Class))
g.add((SSO['CrossSectionProfile'], RDFS.label, Literal("Cross-Section Profile", lang="en")))
g.add((SSO['CrossSectionProfile'], RDFS.comment, Literal(
    "The parametric geometric shape of a beam's cross-section — an "
    "abstract type with concrete parametric profiles such as Rectangular, "
    "Box, and I-Profile — assigned to a Beam Section.", lang="en")))

g.add((SSO['RectProfile'], RDF.type, OWL.Class))
g.add((SSO['RectProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['RectProfile'], RDFS.label, Literal("Rectangular Profile", lang="en")))
g.add((SSO['RectProfile'], RDFS.comment, Literal(
    "A solid rectangular cross-section, defined by its width and height.", lang="en")))

g.add((SSO['BoxProfile'], RDF.type, OWL.Class))
g.add((SSO['BoxProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['BoxProfile'], RDFS.label, Literal("Box Profile", lang="en")))
g.add((SSO['BoxProfile'], RDFS.comment, Literal(
    "A rectangular hollow cross-section, defined by its outer width/height "
    "and wall thicknesses.", lang="en")))

g.add((SSO['PipeProfile'], RDF.type, OWL.Class))
g.add((SSO['PipeProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['PipeProfile'], RDFS.label, Literal("Pipe Profile", lang="en")))
g.add((SSO['PipeProfile'], RDFS.comment, Literal(
    "A circular hollow cross-section, defined by its outer radius and wall "
    "thickness.", lang="en")))

g.add((SSO['CircProfile'], RDF.type, OWL.Class))
g.add((SSO['CircProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['CircProfile'], RDFS.label, Literal("Circular Profile", lang="en")))
g.add((SSO['CircProfile'], RDFS.comment, Literal(
    "A solid circular cross-section, defined by its radius.", lang="en")))

g.add((SSO['IProfile'], RDF.type, OWL.Class))
g.add((SSO['IProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['IProfile'], RDFS.label, Literal("I-Profile", lang="en")))
g.add((SSO['IProfile'], RDFS.comment, Literal(
    "An I-shaped (wide-flange) cross-section, defined by its overall depth, "
    "flange widths and thicknesses, and web thickness.", lang="en")))

g.add((SSO['LProfile'], RDF.type, OWL.Class))
g.add((SSO['LProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['LProfile'], RDFS.label, Literal("L-Profile", lang="en")))
g.add((SSO['LProfile'], RDFS.comment, Literal(
    "An L-shaped (angle) cross-section, defined by its two leg widths and "
    "thicknesses.", lang="en")))

g.add((SSO['HexProfile'], RDF.type, OWL.Class))
g.add((SSO['HexProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['HexProfile'], RDFS.label, Literal("Hexagonal Profile", lang="en")))
g.add((SSO['HexProfile'], RDFS.comment, Literal(
    "A hexagonal hollow cross-section, defined by its circumscribed radius "
    "and wall thickness.", lang="en")))

g.add((SSO['TrapezoidProfile'], RDF.type, OWL.Class))
g.add((SSO['TrapezoidProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['TrapezoidProfile'], RDFS.label, Literal("Trapezoid Profile", lang="en")))
g.add((SSO['TrapezoidProfile'], RDFS.comment, Literal(
    "A trapezoidal cross-section, defined by its bottom and top widths, "
    "height, and top-edge offset.", lang="en")))

# Covers both OSAM "GENERAL" and "NON LINEAR GENERAL" cross-section types —
# both carry the same parameters (A, I11, I12, I22, J), so one class suffices.
g.add((SSO['GeneralProfile'], RDF.type, OWL.Class))
g.add((SSO['GeneralProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['GeneralProfile'], RDFS.label, Literal("General Profile", lang="en")))
g.add((SSO['GeneralProfile'], RDFS.comment, Literal(
    "A cross-section defined directly by its section properties (area, "
    "moments of inertia, torsional constant) rather than by shape.", lang="en")))

# Polygon geometry (edge_points/void_points) is not structurally modeled —
# RDF has no native ordered-list-of-points primitive worth the complexity here.
g.add((SSO['ArbitraryProfile'], RDF.type, OWL.Class))
g.add((SSO['ArbitraryProfile'], RDFS.subClassOf, SSO.CrossSectionProfile))
g.add((SSO['ArbitraryProfile'], RDFS.label, Literal("Arbitrary Profile", lang="en")))
g.add((SSO['ArbitraryProfile'], RDFS.comment, Literal(
    "An arbitrary polygonal cross-section, optionally with holes; its point "
    "geometry isn't structurally modeled in this ontology.", lang="en")))

# ── Load subtypes ──────────────────────────────────────────────────────────

g.add((SSO['PointLoad'], RDF.type, OWL.Class))
g.add((SSO['PointLoad'], RDFS.subClassOf, SSO.Load))
g.add((SSO['PointLoad'], RDFS.label, Literal("Point Load", lang="en")))
g.add((SSO['PointLoad'], RDFS.comment, Literal(
    "A concentrated load applied to a single degree of freedom of a node "
    "set.", lang="en")))

g.add((SSO['DistributedLoad'], RDF.type, OWL.Class))
g.add((SSO['DistributedLoad'], RDFS.subClassOf, SSO.Load))
g.add((SSO['DistributedLoad'], RDFS.label, Literal("Distributed Load", lang="en")))
g.add((SSO['DistributedLoad'], RDFS.comment, Literal(
    "A load distributed linearly along an element edge/line, defined by its "
    "direction and end values.", lang="en")))

g.add((SSO['SurfaceLoad'], RDF.type, OWL.Class))
g.add((SSO['SurfaceLoad'], RDFS.subClassOf, SSO.Load))
g.add((SSO['SurfaceLoad'], RDFS.label, Literal("Surface Load", lang="en")))
g.add((SSO['SurfaceLoad'], RDFS.comment, Literal(
    "A pressure load applied over an element face, defined by its magnitude "
    "and direction.", lang="en")))

# ── Provenance / Calibration ──────────────────────────────────────────────
#
# Calibration — the event that produces a calibrated snapshot. Carries all
# provenance (date, test data, agent) via prov:Activity's own properties.
g.add((SSO['Calibration'], RDF.type, OWL.Class))
g.add((SSO['Calibration'], RDFS.subClassOf, PROV.Activity))
g.add((SSO['Calibration'], RDFS.label, Literal("Calibration", lang="en")))
g.add((SSO['Calibration'], RDFS.comment, Literal(
    "A provenance-bearing event (a prov:Activity) that produces a calibrated "
    "snapshot of a model parameter from a baseline, using measured test data.", lang="en")))


##########################################################
#                  Datatype Porperties                   #
##########################################################

# Shared naming/labeling properties (no rdfs:domain restriction: these are
# reused across many unrelated classes, so restricting their domain would
# make RDFS wrongly infer every subject is simultaneously an instance of
# every class that ever uses them — see StructuralAnalysisModel.id/name below
# for the properties these replace).
#
# rdfs:label -> every "name" field (StructuralAnalysisModel, Object, Assembly,
#   Instance, Material, Section, LoadCase, Nset, Elset, ...)
# dcterms:identifier -> every "id" field (StructuralAnalysisModel, Object,
#   Instance, Section, Load, LoadCase, BoundaryCondition, Node, Element)
# Both are used directly, no local re-declaration needed.

#StructuralAnalysisModel.format
g.add((SSO['format'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['format'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['format'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['format'], RDFS.range, XSD.string))
g.add((SSO['format'], RDFS.label, Literal("format", lang="en")))
g.add((SSO['format'], RDFS.comment, Literal(
    "The serialization format of the model file (e.g. 'ttl').", lang="en")))

#StructuralAnalysisModel.as_OSAM-json
g.add((SSO['as_OSAM-json'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['as_OSAM-json'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['as_OSAM-json'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['as_OSAM-json'], RDFS.range, XSD.string))
g.add((SSO['as_OSAM-json'], RDFS.range, XSD.anyURI))
g.add((SSO['as_OSAM-json'], RDFS.label, Literal("as OSAM JSON", lang="en")))
g.add((SSO['as_OSAM-json'], RDFS.comment, Literal(
    "A link to this model serialized as an O-SAM JSON file.", lang="en")))

#StructuralAnalysisModel.as_abaqus-inp
g.add((SSO['as_abaqus-inp'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['as_abaqus-inp'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['as_abaqus-inp'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['as_abaqus-inp'], RDFS.range, XSD.string))
g.add((SSO['as_abaqus-inp'], RDFS.range, XSD.anyURI))
g.add((SSO['as_abaqus-inp'], RDFS.label, Literal("as Abaqus INP", lang="en")))
g.add((SSO['as_abaqus-inp'], RDFS.comment, Literal(
    "A link to this model serialized as an Abaqus .inp input file.", lang="en")))

#StructuralAnalysisModel.as_ifc-sa
g.add((SSO['as_ifc-sa'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['as_ifc-sa'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['as_ifc-sa'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['as_ifc-sa'], RDFS.range, XSD.string))
g.add((SSO['as_ifc-sa'], RDFS.range, XSD.anyURI))
g.add((SSO['as_ifc-sa'], RDFS.label, Literal("as IFC Structural Analysis", lang="en")))
g.add((SSO['as_ifc-sa'], RDFS.comment, Literal(
    "A link to this model serialized as an IFC structural-analysis-domain "
    "file.", lang="en")))

#StructuralAnalysisModel.creation_date
g.add((SSO['creation_date'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['creation_date'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['creation_date'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['creation_date'], RDFS.range, XSD.dateTimeStamp))
g.add((SSO['creation_date'], RDFS.range, XSD.dateTime))
g.add((SSO['creation_date'], RDFS.label, Literal("creation date", lang="en")))
g.add((SSO['creation_date'], RDFS.comment, Literal(
    "The date and time the Structural Analysis Model was created.", lang="en")))

#Mesh.node_count / Element.node_count (shared: both Mesh and Element have a
#node count, and they aren't related by subclassing, so no domain restriction)
g.add((SSO['node_count'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['node_count'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['node_count'], RDFS.range, XSD.integer))
g.add((SSO['node_count'], RDFS.label, Literal("node count", lang="en")))
g.add((SSO['node_count'], RDFS.comment, Literal(
    "The number of nodes in a Mesh, or referenced by an Element.", lang="en")))

#Mesh.el_count
g.add((SSO['el_count'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['el_count'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['el_count'], RDFS.domain, SSO.Mesh))
g.add((SSO['el_count'], RDFS.range, XSD.integer))
g.add((SSO['el_count'], RDFS.label, Literal("element count", lang="en")))
g.add((SSO['el_count'], RDFS.comment, Literal(
    "The number of elements in a Mesh.", lang="en")))

#Node.X / Vector3D.X (shared coordinate properties: Node and Vector3D aren't
#related by subclassing, so no domain restriction)
g.add((SSO['X'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['X'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['X'], RDFS.range, XSD.float))
g.add((SSO['X'], RDFS.label, Literal("X coordinate", lang="en")))
g.add((SSO['X'], RDFS.comment, Literal(
    "The X component of a Node's position or a 3D Vector.", lang="en")))

#Node.Y / Vector3D.Y
g.add((SSO['Y'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['Y'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['Y'], RDFS.range, XSD.float))
g.add((SSO['Y'], RDFS.label, Literal("Y coordinate", lang="en")))
g.add((SSO['Y'], RDFS.comment, Literal(
    "The Y component of a Node's position or a 3D Vector.", lang="en")))

#Node.Z / Vector3D.Z
g.add((SSO['Z'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['Z'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['Z'], RDFS.range, XSD.float))
g.add((SSO['Z'], RDFS.label, Literal("Z coordinate", lang="en")))
g.add((SSO['Z'], RDFS.comment, Literal(
    "The Z component of a Node's position or a 3D Vector.", lang="en")))

#Units.force
g.add((SSO['force'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['force'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['force'], RDFS.domain, SSO.Units))
g.add((SSO['force'], RDFS.range, XSD.string))
g.add((SSO['force'], RDFS.label, Literal("force unit", lang="en")))
g.add((SSO['force'], RDFS.comment, Literal(
    "The unit of force used by the model (e.g. 'KILONEWTON').", lang="en")))

#Units.length
g.add((SSO['length'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['length'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['length'], RDFS.domain, SSO.Units))
g.add((SSO['length'], RDFS.range, XSD.string))
g.add((SSO['length'], RDFS.label, Literal("length unit", lang="en")))
g.add((SSO['length'], RDFS.comment, Literal(
    "The unit of length used by the model (e.g. 'METRE').", lang="en")))

#Units.temperature
g.add((SSO['temperature'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['temperature'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['temperature'], RDFS.domain, SSO.Units))
g.add((SSO['temperature'], RDFS.range, XSD.string))
g.add((SSO['temperature'], RDFS.label, Literal("temperature unit", lang="en")))
g.add((SSO['temperature'], RDFS.comment, Literal(
    "The unit of temperature used by the model (e.g. 'CELSIUS').", lang="en")))

#Units.time
g.add((SSO['time'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['time'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['time'], RDFS.domain, SSO.Units))
g.add((SSO['time'], RDFS.range, XSD.string))
g.add((SSO['time'], RDFS.label, Literal("time unit", lang="en")))
g.add((SSO['time'], RDFS.comment, Literal(
    "The unit of time used by the model (e.g. 'SECOND').", lang="en")))

#Units.mass
g.add((SSO['mass'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['mass'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['mass'], RDFS.domain, SSO.Units))
g.add((SSO['mass'], RDFS.range, XSD.string))
g.add((SSO['mass'], RDFS.label, Literal("mass unit", lang="en")))
g.add((SSO['mass'], RDFS.comment, Literal(
    "The unit of mass used by the model (e.g. 'KILOGRAM').", lang="en")))

#Element.face_count
g.add((SSO['face_count'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['face_count'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['face_count'], RDFS.domain, SSO.Element))
g.add((SSO['face_count'], RDFS.range, XSD.integer))
g.add((SSO['face_count'], RDFS.label, Literal("face count", lang="en")))
g.add((SSO['face_count'], RDFS.comment, Literal(
    "The number of faces of an element, relevant to solid and shell "
    "elements.", lang="en")))

#Element.dofs (list of active local DOFs, so NOT functional)
g.add((SSO['dofs'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['dofs'], RDFS.domain, SSO.Element))
g.add((SSO['dofs'], RDFS.range, XSD.integer))
g.add((SSO['dofs'], RDFS.label, Literal("degrees of freedom", lang="en")))
g.add((SSO['dofs'], RDFS.comment, Literal(
    "The local degrees of freedom active at an element's nodes.", lang="en")))

#Element.type (raw element type code, e.g. "C3D8", "S4", "B31")
g.add((SSO['element_type'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['element_type'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['element_type'], RDFS.domain, SSO.Element))
g.add((SSO['element_type'], RDFS.range, XSD.string))
g.add((SSO['element_type'], RDFS.label, Literal("element type code", lang="en")))
g.add((SSO['element_type'], RDFS.comment, Literal(
    "The raw finite element type code (e.g. 'C3D8', 'S4', 'B31') identifying "
    "the element's formulation.", lang="en")))

#Element.integration
g.add((SSO['integration'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['integration'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['integration'], RDFS.domain, SSO.Element))
g.add((SSO['integration'], RDFS.range, XSD.string))
g.add((SSO['integration'], RDFS.label, Literal("integration scheme", lang="en")))
g.add((SSO['integration'], RDFS.comment, Literal(
    "The numerical integration scheme used for an element (e.g. 'REDUCED', "
    "'FULL').", lang="en")))

#Instance.translation (OSAM itself leaves this untyped/Any, so its shape is
#not constrained here either)
g.add((SSO['translation'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['translation'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['translation'], RDFS.domain, SSO.Instance))
g.add((SSO['translation'], RDFS.range, RDFS.Literal))
g.add((SSO['translation'], RDFS.label, Literal("translation", lang="en")))
g.add((SSO['translation'], RDFS.comment, Literal(
    "The translation applied to an Instance when placing its Object in the "
    "Assembly.", lang="en")))

#Instance.rotation
g.add((SSO['rotation'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['rotation'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['rotation'], RDFS.domain, SSO.Instance))
g.add((SSO['rotation'], RDFS.range, RDFS.Literal))
g.add((SSO['rotation'], RDFS.label, Literal("rotation", lang="en")))
g.add((SSO['rotation'], RDFS.comment, Literal(
    "The rotation applied to an Instance when placing its Object in the "
    "Assembly.", lang="en")))

#Material.category
g.add((SSO['material_category'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['material_category'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['material_category'], RDFS.domain, SSO.Material))
g.add((SSO['material_category'], RDFS.range, XSD.string))
g.add((SSO['material_category'], RDFS.label, Literal("material category", lang="en")))
g.add((SSO['material_category'], RDFS.comment, Literal(
    "A broad classification of the material (e.g. concrete, steel, timber).", lang="en")))

#Material.type
g.add((SSO['material_type'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['material_type'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['material_type'], RDFS.domain, SSO.Material))
g.add((SSO['material_type'], RDFS.range, XSD.string))
g.add((SSO['material_type'], RDFS.label, Literal("material type", lang="en")))
g.add((SSO['material_type'], RDFS.comment, Literal(
    "The material's constitutive type (e.g. 'ISOTROPIC').", lang="en")))

#Material.mass_density
g.add((SSO['mass_density'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['mass_density'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['mass_density'], RDFS.domain, SSO.Material))
g.add((SSO['mass_density'], RDFS.range, XSD.float))
g.add((SSO['mass_density'], RDFS.label, Literal("mass density", lang="en")))
g.add((SSO['mass_density'], RDFS.comment, Literal(
    "The material's mass per unit volume, used e.g. to compute self-weight "
    "loads.", lang="en")))

#ElasticBehaviour.behaviour_type
g.add((SSO['behaviour_type'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['behaviour_type'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['behaviour_type'], RDFS.domain, SSO.ElasticBehaviour))
g.add((SSO['behaviour_type'], RDFS.range, XSD.string))
g.add((SSO['behaviour_type'], RDFS.label, Literal("elastic behaviour type", lang="en")))
g.add((SSO['behaviour_type'], RDFS.comment, Literal(
    "The constitutive symmetry class of the elastic behaviour — ISOTROPIC, "
    "ANISOTROPIC, or ORTHOTROPIC.", lang="en")))

#ElasticBehaviour.E
g.add((SSO['E'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['E'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['E'], RDFS.domain, SSO.ElasticBehaviour))
g.add((SSO['E'], RDFS.range, XSD.float))
g.add((SSO['E'], RDFS.label, Literal("Young's modulus", lang="en")))
g.add((SSO['E'], RDFS.comment, Literal(
    "The material's Young's modulus (modulus of elasticity), relating stress "
    "to strain in the elastic range.", lang="en")))

#ElasticBehaviour.poisson_ratio (OSAM field name is bare "v"; renamed here
#because "v" is already used for Load's magnitude property, see below)
g.add((SSO['poisson_ratio'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['poisson_ratio'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['poisson_ratio'], RDFS.domain, SSO.ElasticBehaviour))
g.add((SSO['poisson_ratio'], RDFS.range, XSD.float))
g.add((SSO['poisson_ratio'], RDFS.label, Literal("Poisson's ratio", lang="en")))
g.add((SSO['poisson_ratio'], RDFS.comment, Literal(
    "The material's Poisson's ratio, the ratio of transverse to axial strain "
    "in the elastic range.", lang="en")))

#PlasticBehaviour.yield_stress
g.add((SSO['yield_stress'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['yield_stress'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['yield_stress'], RDFS.domain, SSO.PlasticBehaviour))
g.add((SSO['yield_stress'], RDFS.range, XSD.float))
g.add((SSO['yield_stress'], RDFS.label, Literal("yield stress", lang="en")))
g.add((SSO['yield_stress'], RDFS.comment, Literal(
    "The stress at which the material begins to deform plastically.", lang="en")))

#PlasticBehaviour.plastic_strain
g.add((SSO['plastic_strain'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['plastic_strain'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['plastic_strain'], RDFS.domain, SSO.PlasticBehaviour))
g.add((SSO['plastic_strain'], RDFS.range, XSD.float))
g.add((SSO['plastic_strain'], RDFS.label, Literal("plastic strain", lang="en")))
g.add((SSO['plastic_strain'], RDFS.comment, Literal(
    "The plastic (permanent) strain corresponding to the yield stress in the "
    "material's plastic behaviour.", lang="en")))

#BeamSection.beam_section
g.add((SSO['beam_section'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['beam_section'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['beam_section'], RDFS.domain, SSO.BeamSection))
g.add((SSO['beam_section'], RDFS.range, XSD.string))
g.add((SSO['beam_section'], RDFS.label, Literal("beam section name", lang="en")))
g.add((SSO['beam_section'], RDFS.comment, Literal(
    "The name of the named beam profile (e.g. a catalog section like "
    "'IPE200') assigned to a Beam Section.", lang="en")))

#ShellSection.thickness
g.add((SSO['thickness'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['thickness'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['thickness'], RDFS.domain, SSO.ShellSection))
g.add((SSO['thickness'], RDFS.range, XSD.float))
g.add((SSO['thickness'], RDFS.label, Literal("thickness", lang="en")))
g.add((SSO['thickness'], RDFS.comment, Literal(
    "The shell section's thickness.", lang="en")))

#RectProfile.a / BoxProfile.a / LProfile.a / TrapezoidProfile.a (shared:
#sibling subclasses of CrossSectionProfile, so domain is the common parent)
g.add((SSO['a'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['a'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['a'], RDFS.domain, SSO.CrossSectionProfile))
g.add((SSO['a'], RDFS.range, XSD.float))
g.add((SSO['a'], RDFS.label, Literal("dimension a", lang="en")))
g.add((SSO['a'], RDFS.comment, Literal(
    "A cross-section's primary planar dimension (e.g. width for a "
    "rectangular or box profile, a leg length for an angle, the bottom "
    "width for a trapezoid) — its exact geometric role depends on the "
    "profile shape.", lang="en")))

#RectProfile.b / BoxProfile.b / LProfile.b / TrapezoidProfile.b
g.add((SSO['b'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['b'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['b'], RDFS.domain, SSO.CrossSectionProfile))
g.add((SSO['b'], RDFS.range, XSD.float))
g.add((SSO['b'], RDFS.label, Literal("dimension b", lang="en")))
g.add((SSO['b'], RDFS.comment, Literal(
    "A cross-section's secondary planar dimension (e.g. height for a "
    "rectangular or box profile, the other leg length for an angle, the top "
    "width for a trapezoid) — its exact geometric role depends on the "
    "profile shape.", lang="en")))

#BoxProfile.t1 / IProfile.t1 / LProfile.t1
g.add((SSO['t1'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['t1'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['t1'], RDFS.domain, SSO.CrossSectionProfile))
g.add((SSO['t1'], RDFS.range, XSD.float))
g.add((SSO['t1'], RDFS.label, Literal("wall/flange thickness t1", lang="en")))
g.add((SSO['t1'], RDFS.comment, Literal(
    "A wall or flange thickness of a cross-section profile (box, I, or L) — "
    "its exact location depends on the profile shape.", lang="en")))

#BoxProfile.t2 / IProfile.t2 / LProfile.t2
g.add((SSO['t2'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['t2'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['t2'], RDFS.domain, SSO.CrossSectionProfile))
g.add((SSO['t2'], RDFS.range, XSD.float))
g.add((SSO['t2'], RDFS.label, Literal("wall/flange thickness t2", lang="en")))
g.add((SSO['t2'], RDFS.comment, Literal(
    "A second wall or flange thickness of a cross-section profile (box, I, "
    "or L) — its exact location depends on the profile shape.", lang="en")))

#BoxProfile.t3 / IProfile.t3
g.add((SSO['t3'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['t3'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['t3'], RDFS.domain, SSO.CrossSectionProfile))
g.add((SSO['t3'], RDFS.range, XSD.float))
g.add((SSO['t3'], RDFS.label, Literal("wall/web thickness t3", lang="en")))
g.add((SSO['t3'], RDFS.comment, Literal(
    "A third wall thickness (box profile) or web thickness (I profile), "
    "depending on the profile shape.", lang="en")))

#BoxProfile.t4
g.add((SSO['t4'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['t4'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['t4'], RDFS.domain, SSO.BoxProfile))
g.add((SSO['t4'], RDFS.range, XSD.float))
g.add((SSO['t4'], RDFS.label, Literal("wall thickness t4", lang="en")))
g.add((SSO['t4'], RDFS.comment, Literal(
    "The fourth wall thickness of a box profile.", lang="en")))

#PipeProfile.r / HexProfile's circ_r is separate, see below
g.add((SSO['r'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['r'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['r'], RDFS.domain, SSO.PipeProfile))
g.add((SSO['r'], RDFS.range, XSD.float))
g.add((SSO['r'], RDFS.label, Literal("outer radius", lang="en")))
g.add((SSO['r'], RDFS.comment, Literal(
    "The outer radius of a pipe (circular hollow) profile.", lang="en")))

#PipeProfile.t / HexProfile.t
g.add((SSO['t'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['t'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['t'], RDFS.domain, SSO.CrossSectionProfile))
g.add((SSO['t'], RDFS.range, XSD.float))
g.add((SSO['t'], RDFS.label, Literal("wall thickness", lang="en")))
g.add((SSO['t'], RDFS.comment, Literal(
    "The wall thickness of a pipe or hexagonal hollow profile.", lang="en")))

#CircProfile.radius
g.add((SSO['radius'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['radius'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['radius'], RDFS.domain, SSO.CircProfile))
g.add((SSO['radius'], RDFS.range, XSD.float))
g.add((SSO['radius'], RDFS.label, Literal("radius", lang="en")))
g.add((SSO['radius'], RDFS.comment, Literal(
    "The radius of a solid circular profile.", lang="en")))

#IProfile.h
g.add((SSO['h'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['h'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['h'], RDFS.domain, SSO.IProfile))
g.add((SSO['h'], RDFS.range, XSD.float))
g.add((SSO['h'], RDFS.label, Literal("depth", lang="en")))
g.add((SSO['h'], RDFS.comment, Literal(
    "The overall depth of an I-shaped profile.", lang="en")))

#IProfile.b1
g.add((SSO['b1'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['b1'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['b1'], RDFS.domain, SSO.IProfile))
g.add((SSO['b1'], RDFS.range, XSD.float))
g.add((SSO['b1'], RDFS.label, Literal("flange width b1", lang="en")))
g.add((SSO['b1'], RDFS.comment, Literal(
    "The width of the first flange of an I-shaped profile.", lang="en")))

#IProfile.b2
g.add((SSO['b2'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['b2'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['b2'], RDFS.domain, SSO.IProfile))
g.add((SSO['b2'], RDFS.range, XSD.float))
g.add((SSO['b2'], RDFS.label, Literal("flange width b2", lang="en")))
g.add((SSO['b2'], RDFS.comment, Literal(
    "The width of the second flange of an I-shaped profile.", lang="en")))

#IProfile.l (optional Abaqus flange-offset parameter)
g.add((SSO['l'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['l'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['l'], RDFS.domain, SSO.IProfile))
g.add((SSO['l'], RDFS.range, XSD.float))
g.add((SSO['l'], RDFS.label, Literal("flange offset", lang="en")))
g.add((SSO['l'], RDFS.comment, Literal(
    "The optional Abaqus flange-offset parameter of an I-shaped profile.", lang="en")))

#HexProfile.circ_r
g.add((SSO['circ_r'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['circ_r'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['circ_r'], RDFS.domain, SSO.HexProfile))
g.add((SSO['circ_r'], RDFS.range, XSD.float))
g.add((SSO['circ_r'], RDFS.label, Literal("circumscribed radius", lang="en")))
g.add((SSO['circ_r'], RDFS.comment, Literal(
    "The circumscribed radius of a hexagonal hollow profile.", lang="en")))

#TrapezoidProfile.c
g.add((SSO['c'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['c'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['c'], RDFS.domain, SSO.TrapezoidProfile))
g.add((SSO['c'], RDFS.range, XSD.float))
g.add((SSO['c'], RDFS.label, Literal("height c", lang="en")))
g.add((SSO['c'], RDFS.comment, Literal(
    "The height of a trapezoidal profile.", lang="en")))

#TrapezoidProfile.d
g.add((SSO['d'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['d'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['d'], RDFS.domain, SSO.TrapezoidProfile))
g.add((SSO['d'], RDFS.range, XSD.float))
g.add((SSO['d'], RDFS.label, Literal("top-edge offset d", lang="en")))
g.add((SSO['d'], RDFS.comment, Literal(
    "The horizontal offset of the top edge of a trapezoidal profile.", lang="en")))

#GeneralProfile.A
g.add((SSO['A'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['A'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['A'], RDFS.domain, SSO.GeneralProfile))
g.add((SSO['A'], RDFS.range, XSD.float))
g.add((SSO['A'], RDFS.label, Literal("cross-sectional area", lang="en")))
g.add((SSO['A'], RDFS.comment, Literal(
    "The cross-sectional area of a General Profile, given directly rather "
    "than derived from shape.", lang="en")))

#GeneralProfile.I11
g.add((SSO['I11'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['I11'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['I11'], RDFS.domain, SSO.GeneralProfile))
g.add((SSO['I11'], RDFS.range, XSD.float))
g.add((SSO['I11'], RDFS.label, Literal("moment of inertia I11", lang="en")))
g.add((SSO['I11'], RDFS.comment, Literal(
    "The moment of inertia about the section's first principal axis, for a "
    "General Profile.", lang="en")))

#GeneralProfile.I12
g.add((SSO['I12'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['I12'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['I12'], RDFS.domain, SSO.GeneralProfile))
g.add((SSO['I12'], RDFS.range, XSD.float))
g.add((SSO['I12'], RDFS.label, Literal("product of inertia I12", lang="en")))
g.add((SSO['I12'], RDFS.comment, Literal(
    "The product of inertia of a General Profile's cross-section.", lang="en")))

#GeneralProfile.I22
g.add((SSO['I22'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['I22'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['I22'], RDFS.domain, SSO.GeneralProfile))
g.add((SSO['I22'], RDFS.range, XSD.float))
g.add((SSO['I22'], RDFS.label, Literal("moment of inertia I22", lang="en")))
g.add((SSO['I22'], RDFS.comment, Literal(
    "The moment of inertia about the section's second principal axis, for a "
    "General Profile.", lang="en")))

#GeneralProfile.J
g.add((SSO['J'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['J'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['J'], RDFS.domain, SSO.GeneralProfile))
g.add((SSO['J'], RDFS.range, XSD.float))
g.add((SSO['J'], RDFS.label, Literal("torsional constant", lang="en")))
g.add((SSO['J'], RDFS.comment, Literal(
    "The torsional constant of a General Profile's cross-section.", lang="en")))

#LoadCase.type
g.add((SSO['loadCase_type'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['loadCase_type'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['loadCase_type'], RDFS.domain, SSO.LoadCase))
g.add((SSO['loadCase_type'], RDFS.range, XSD.string))
g.add((SSO['loadCase_type'], RDFS.label, Literal("load case type", lang="en")))
g.add((SSO['loadCase_type'], RDFS.comment, Literal(
    "The type of a Load Case (e.g. static, dynamic).", lang="en")))

#PointLoad.dof
g.add((SSO['dof'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['dof'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['dof'], RDFS.domain, SSO.PointLoad))
g.add((SSO['dof'], RDFS.range, XSD.integer))
g.add((SSO['dof'], RDFS.label, Literal("degree of freedom", lang="en")))
g.add((SSO['dof'], RDFS.comment, Literal(
    "The local degree of freedom index a Point Load is applied to.", lang="en")))

#PointLoad.v / SurfaceLoad.v (shared: sibling subclasses of Load)
g.add((SSO['v'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['v'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['v'], RDFS.domain, SSO.Load))
g.add((SSO['v'], RDFS.range, XSD.float))
g.add((SSO['v'], RDFS.label, Literal("load magnitude", lang="en")))
g.add((SSO['v'], RDFS.comment, Literal(
    "The magnitude of a Point Load or Surface Load.", lang="en")))

#DistributedLoad.dir
g.add((SSO['dir'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['dir'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['dir'], RDFS.domain, SSO.DistributedLoad))
g.add((SSO['dir'], RDFS.range, XSD.string))
g.add((SSO['dir'], RDFS.label, Literal("distribution direction", lang="en")))
g.add((SSO['dir'], RDFS.comment, Literal(
    "The direction along which a Distributed Load varies.", lang="en")))

#DistributedLoad.v1
g.add((SSO['v1'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['v1'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['v1'], RDFS.domain, SSO.DistributedLoad))
g.add((SSO['v1'], RDFS.range, XSD.float))
g.add((SSO['v1'], RDFS.label, Literal("start value v1", lang="en")))
g.add((SSO['v1'], RDFS.comment, Literal(
    "The Distributed Load's value at its start point.", lang="en")))

#DistributedLoad.v2
g.add((SSO['v2'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['v2'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['v2'], RDFS.domain, SSO.DistributedLoad))
g.add((SSO['v2'], RDFS.range, XSD.float))
g.add((SSO['v2'], RDFS.label, Literal("end value v2", lang="en")))
g.add((SSO['v2'], RDFS.comment, Literal(
    "The Distributed Load's value at its end point.", lang="en")))

#DistributedLoad.x1
g.add((SSO['x1'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['x1'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['x1'], RDFS.domain, SSO.DistributedLoad))
g.add((SSO['x1'], RDFS.range, XSD.float))
g.add((SSO['x1'], RDFS.label, Literal("start position x1", lang="en")))
g.add((SSO['x1'], RDFS.comment, Literal(
    "The position along the element where a Distributed Load's start value "
    "applies.", lang="en")))

#DistributedLoad.x2
g.add((SSO['x2'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['x2'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['x2'], RDFS.domain, SSO.DistributedLoad))
g.add((SSO['x2'], RDFS.range, XSD.float))
g.add((SSO['x2'], RDFS.label, Literal("end position x2", lang="en")))
g.add((SSO['x2'], RDFS.comment, Literal(
    "The position along the element where a Distributed Load's end value "
    "applies.", lang="en")))

#SurfaceLoad.xdir
g.add((SSO['xdir'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['xdir'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['xdir'], RDFS.domain, SSO.SurfaceLoad))
g.add((SSO['xdir'], RDFS.range, XSD.float))
g.add((SSO['xdir'], RDFS.label, Literal("X direction component", lang="en")))
g.add((SSO['xdir'], RDFS.comment, Literal(
    "The X component of a Surface Load's direction vector.", lang="en")))

#SurfaceLoad.ydir
g.add((SSO['ydir'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['ydir'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['ydir'], RDFS.domain, SSO.SurfaceLoad))
g.add((SSO['ydir'], RDFS.range, XSD.float))
g.add((SSO['ydir'], RDFS.label, Literal("Y direction component", lang="en")))
g.add((SSO['ydir'], RDFS.comment, Literal(
    "The Y component of a Surface Load's direction vector.", lang="en")))

#SurfaceLoad.zdir
g.add((SSO['zdir'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['zdir'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['zdir'], RDFS.domain, SSO.SurfaceLoad))
g.add((SSO['zdir'], RDFS.range, XSD.float))
g.add((SSO['zdir'], RDFS.label, Literal("Z direction component", lang="en")))
g.add((SSO['zdir'], RDFS.comment, Literal(
    "The Z component of a Surface Load's direction vector.", lang="en")))

#BoundaryCondition.type
g.add((SSO['bc_type'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['bc_type'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['bc_type'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['bc_type'], RDFS.range, XSD.string))
g.add((SSO['bc_type'], RDFS.label, Literal("boundary condition type", lang="en")))
g.add((SSO['bc_type'], RDFS.comment, Literal(
    "The type of a Boundary Condition (e.g. 'DISPLACEMENT').", lang="en")))

# BoundaryCondition DOF fields: each OSAM ux/uy/uz/rx/ry/rz is either a bool
# (free/fixed) or a float (a prescribed displacement value) — split into a
# "restrained" flag and an optional "prescribed" value per DOF.

#BoundaryCondition.ux
g.add((SSO['restrained_ux'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['restrained_ux'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['restrained_ux'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['restrained_ux'], RDFS.range, XSD.boolean))
g.add((SSO['restrained_ux'], RDFS.label, Literal("restrained (ux)", lang="en")))
g.add((SSO['restrained_ux'], RDFS.comment, Literal(
    "Whether the boundary condition constrains translation along X.", lang="en")))

g.add((SSO['prescribed_ux'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['prescribed_ux'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['prescribed_ux'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['prescribed_ux'], RDFS.range, XSD.float))
g.add((SSO['prescribed_ux'], RDFS.label, Literal("prescribed displacement (ux)", lang="en")))
g.add((SSO['prescribed_ux'], RDFS.comment, Literal(
    "The prescribed translation value along X, when the boundary condition "
    "imposes a displacement rather than a simple restraint.", lang="en")))

#BoundaryCondition.uy
g.add((SSO['restrained_uy'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['restrained_uy'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['restrained_uy'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['restrained_uy'], RDFS.range, XSD.boolean))
g.add((SSO['restrained_uy'], RDFS.label, Literal("restrained (uy)", lang="en")))
g.add((SSO['restrained_uy'], RDFS.comment, Literal(
    "Whether the boundary condition constrains translation along Y.", lang="en")))

g.add((SSO['prescribed_uy'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['prescribed_uy'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['prescribed_uy'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['prescribed_uy'], RDFS.range, XSD.float))
g.add((SSO['prescribed_uy'], RDFS.label, Literal("prescribed displacement (uy)", lang="en")))
g.add((SSO['prescribed_uy'], RDFS.comment, Literal(
    "The prescribed translation value along Y, when the boundary condition "
    "imposes a displacement rather than a simple restraint.", lang="en")))

#BoundaryCondition.uz
g.add((SSO['restrained_uz'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['restrained_uz'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['restrained_uz'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['restrained_uz'], RDFS.range, XSD.boolean))
g.add((SSO['restrained_uz'], RDFS.label, Literal("restrained (uz)", lang="en")))
g.add((SSO['restrained_uz'], RDFS.comment, Literal(
    "Whether the boundary condition constrains translation along Z.", lang="en")))

g.add((SSO['prescribed_uz'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['prescribed_uz'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['prescribed_uz'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['prescribed_uz'], RDFS.range, XSD.float))
g.add((SSO['prescribed_uz'], RDFS.label, Literal("prescribed displacement (uz)", lang="en")))
g.add((SSO['prescribed_uz'], RDFS.comment, Literal(
    "The prescribed translation value along Z, when the boundary condition "
    "imposes a displacement rather than a simple restraint.", lang="en")))

#BoundaryCondition.rx
g.add((SSO['restrained_rx'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['restrained_rx'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['restrained_rx'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['restrained_rx'], RDFS.range, XSD.boolean))
g.add((SSO['restrained_rx'], RDFS.label, Literal("restrained (rx)", lang="en")))
g.add((SSO['restrained_rx'], RDFS.comment, Literal(
    "Whether the boundary condition constrains rotation about X.", lang="en")))

g.add((SSO['prescribed_rx'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['prescribed_rx'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['prescribed_rx'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['prescribed_rx'], RDFS.range, XSD.float))
g.add((SSO['prescribed_rx'], RDFS.label, Literal("prescribed rotation (rx)", lang="en")))
g.add((SSO['prescribed_rx'], RDFS.comment, Literal(
    "The prescribed rotation value about X, when the boundary condition "
    "imposes a rotation rather than a simple restraint.", lang="en")))

#BoundaryCondition.ry
g.add((SSO['restrained_ry'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['restrained_ry'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['restrained_ry'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['restrained_ry'], RDFS.range, XSD.boolean))
g.add((SSO['restrained_ry'], RDFS.label, Literal("restrained (ry)", lang="en")))
g.add((SSO['restrained_ry'], RDFS.comment, Literal(
    "Whether the boundary condition constrains rotation about Y.", lang="en")))

g.add((SSO['prescribed_ry'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['prescribed_ry'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['prescribed_ry'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['prescribed_ry'], RDFS.range, XSD.float))
g.add((SSO['prescribed_ry'], RDFS.label, Literal("prescribed rotation (ry)", lang="en")))
g.add((SSO['prescribed_ry'], RDFS.comment, Literal(
    "The prescribed rotation value about Y, when the boundary condition "
    "imposes a rotation rather than a simple restraint.", lang="en")))

#BoundaryCondition.rz
g.add((SSO['restrained_rz'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['restrained_rz'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['restrained_rz'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['restrained_rz'], RDFS.range, XSD.boolean))
g.add((SSO['restrained_rz'], RDFS.label, Literal("restrained (rz)", lang="en")))
g.add((SSO['restrained_rz'], RDFS.comment, Literal(
    "Whether the boundary condition constrains rotation about Z.", lang="en")))

g.add((SSO['prescribed_rz'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['prescribed_rz'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['prescribed_rz'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['prescribed_rz'], RDFS.range, XSD.float))
g.add((SSO['prescribed_rz'], RDFS.label, Literal("prescribed rotation (rz)", lang="en")))
g.add((SSO['prescribed_rz'], RDFS.comment, Literal(
    "The prescribed rotation value about Z, when the boundary condition "
    "imposes a rotation rather than a simple restraint.", lang="en")))


##########################################################
#                   ObjectType Porperties                    #
##########################################################

#StructuralAnalysisModel.referenced_in_sam
g.add((SSO['referenced_in_sam'], RDF.type, OWL.ObjectProperty))
g.add((SSO['referenced_in_sam'], RDFS.domain, OWL.Thing))
g.add((SSO['referenced_in_sam'], RDFS.seeAlso, BEO.BuiltElement))
g.add((SSO['referenced_in_sam'], RDFS.seeAlso, BOT.Element))
g.add((SSO['referenced_in_sam'], RDFS.seeAlso, BOT.Zone))
g.add((SSO['referenced_in_sam'], RDFS.seeAlso, BROT.Bridge))
g.add((SSO['referenced_in_sam'], RDFS.range, SSO['StructuralAnalysisModel']))
g.add((SSO['referenced_in_sam'], RDFS.label, Literal("referenced in SAM", lang="en")))
g.add((SSO['referenced_in_sam'], RDFS.comment, Literal(
    "Links any resource (e.g. a building, bridge, space, or building element "
    "from an external ontology) to the Structural Analysis Model that "
    "simulates it. Domain is intentionally open.", lang="en")))

#idealized_by: links an external building element (e.g. beo:Slab,
#bot:Element) to the SSO finite elements that idealize it in a structural
#analysis model (e.g. a set of sso:ShellElement). Domain left open, same
#pattern as referenced_in_sam, so it works with any external element class.
g.add((SSO['idealized_by'], RDF.type, OWL.ObjectProperty))
g.add((SSO['idealized_by'], RDFS.range, SSO.Element))
g.add((SSO['idealized_by'], RDFS.seeAlso, BEO.BuiltElement))
g.add((SSO['idealized_by'], RDFS.seeAlso, BOT.Element))
g.add((SSO['idealized_by'], RDFS.label, Literal("idealized by", lang="en")))
g.add((SSO['idealized_by'], RDFS.comment, Literal(
    "Links an external built element (e.g. beo:Slab, bot:Element) to the SSO "
    "finite elements that idealize it in a structural analysis model (e.g. a "
    "set of Shell Elements). Domain is intentionally open.", lang="en")))

#has_calibration — entity -> Calibration event(s) it has undergone. Open
#domain (any class can be calibrated). Non-functional: an entity can
#accumulate several calibrations over time. Inverse of prov:used.
g.add((SSO['has_calibration'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_calibration'], RDFS.range, SSO.Calibration))
g.add((SSO['has_calibration'], OWL.inverseOf, PROV.used))
g.add((SSO['has_calibration'], RDFS.label, Literal("has calibration", lang="en")))
g.add((SSO['has_calibration'], RDFS.comment, Literal(
    "Links an entity to the Calibration event(s) it has undergone; an entity "
    "may accumulate several calibrations over time. Domain is intentionally "
    "open, and it is the inverse of prov:used.", lang="en")))

#calibrated_by — calibrated entity -> the Calibration that produced it.
#Open domain. Functional (one producing event per snapshot). Sub-property
#of prov:wasGeneratedBy for PROV reasoning.
g.add((SSO['calibrated_by'], RDF.type, OWL.ObjectProperty))
g.add((SSO['calibrated_by'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['calibrated_by'], RDFS.subPropertyOf, PROV.wasGeneratedBy))
g.add((SSO['calibrated_by'], RDFS.range, SSO.Calibration))
g.add((SSO['calibrated_by'], RDFS.label, Literal("calibrated by", lang="en")))
g.add((SSO['calibrated_by'], RDFS.comment, Literal(
    "Links a calibrated entity (e.g. a Material's Elastic Behaviour, a "
    "Boundary Condition) to the Calibration event that produced this "
    "snapshot of it. Domain is intentionally open.", lang="en")))

#StructuralAnalysisModel.has_object
g.add((SSO['has_object'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_object'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_object'], RDFS.range, SSO.Object))
g.add((SSO['has_object'], RDFS.label, Literal("has object", lang="en")))
g.add((SSO['has_object'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to one of its constituent Objects.", lang="en")))

#StructuralAnalysisModel.has_assembly
g.add((SSO['has_assembly'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_assembly'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_assembly'], RDFS.range, SSO.Assembly))
g.add((SSO['has_assembly'], RDFS.label, Literal("has assembly", lang="en")))
g.add((SSO['has_assembly'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to its Assembly.", lang="en")))

#StructuralAnalysisModel.has_material
g.add((SSO['has_material'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_material'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_material'], RDFS.range, SSO.Material))
g.add((SSO['has_material'], RDFS.label, Literal("has material", lang="en")))
g.add((SSO['has_material'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to one of its Materials.", lang="en")))

#StructuralAnalysisModel.has_section
g.add((SSO['has_section'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_section'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_section'], RDFS.range, SSO.Section))
g.add((SSO['has_section'], RDFS.label, Literal("has section", lang="en")))
g.add((SSO['has_section'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to one of its Sections.", lang="en")))

#StructuralAnalysisModel.has_loadCase
g.add((SSO['has_loadCase'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_loadCase'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_loadCase'], RDFS.range, SSO.LoadCase))
g.add((SSO['has_loadCase'], RDFS.label, Literal("has load case", lang="en")))
g.add((SSO['has_loadCase'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to one of its Load Cases.", lang="en")))

#StructuralAnalysisModel.has_load (the model's flat list of all loads)
g.add((SSO['has_load'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_load'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_load'], RDFS.range, SSO.Load))
g.add((SSO['has_load'], RDFS.label, Literal("has load", lang="en")))
g.add((SSO['has_load'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to one of its Loads.", lang="en")))

#StructuralAnalysisModel.has_boundary_condition
g.add((SSO['has_boundary_condition'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_boundary_condition'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_boundary_condition'], RDFS.range, SSO.BoundaryCondition))
g.add((SSO['has_boundary_condition'], RDFS.label, Literal("has boundary condition", lang="en")))
g.add((SSO['has_boundary_condition'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to one of its Boundary Conditions.", lang="en")))

#StructuralAnalysisModel.has_units
g.add((SSO['has_units'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_units'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_units'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_units'], RDFS.range, SSO.Units))
g.add((SSO['has_units'], RDFS.label, Literal("has units", lang="en")))
g.add((SSO['has_units'], RDFS.comment, Literal(
    "Links a Structural Analysis Model to the Units it is expressed in.", lang="en")))

#Object.has_mesh
g.add((SSO['has_mesh'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_mesh'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_mesh'], RDFS.domain, SSO.Object))
g.add((SSO['has_mesh'], RDFS.range, SSO.Mesh))
g.add((SSO['has_mesh'], RDFS.label, Literal("has mesh", lang="en")))
g.add((SSO['has_mesh'], RDFS.comment, Literal(
    "Links an Object to its Mesh.", lang="en")))

#Object.has_coordinate_system
g.add((SSO['has_coordinate_system'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_coordinate_system'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_coordinate_system'], RDFS.domain, SSO.Object))
g.add((SSO['has_coordinate_system'], RDFS.range, SSO.CoordinateSystem))
g.add((SSO['has_coordinate_system'], RDFS.label, Literal("has coordinate system", lang="en")))
g.add((SSO['has_coordinate_system'], RDFS.comment, Literal(
    "Links an Object to its local Coordinate System.", lang="en")))

#CoordinateSystem.xAxis
g.add((SSO['xAxis'], RDF.type, OWL.ObjectProperty))
g.add((SSO['xAxis'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['xAxis'], RDFS.domain, SSO.CoordinateSystem))
g.add((SSO['xAxis'], RDFS.range, SSO.Vector3D))
g.add((SSO['xAxis'], RDFS.label, Literal("X axis", lang="en")))
g.add((SSO['xAxis'], RDFS.comment, Literal(
    "The Coordinate System's X axis vector.", lang="en")))

#CoordinateSystem.yAxis
g.add((SSO['yAxis'], RDF.type, OWL.ObjectProperty))
g.add((SSO['yAxis'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['yAxis'], RDFS.domain, SSO.CoordinateSystem))
g.add((SSO['yAxis'], RDFS.range, SSO.Vector3D))
g.add((SSO['yAxis'], RDFS.label, Literal("Y axis", lang="en")))
g.add((SSO['yAxis'], RDFS.comment, Literal(
    "The Coordinate System's Y axis vector.", lang="en")))

#CoordinateSystem.zAxis
g.add((SSO['zAxis'], RDF.type, OWL.ObjectProperty))
g.add((SSO['zAxis'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['zAxis'], RDFS.domain, SSO.CoordinateSystem))
g.add((SSO['zAxis'], RDFS.range, SSO.Vector3D))
g.add((SSO['zAxis'], RDFS.label, Literal("Z axis", lang="en")))
g.add((SSO['zAxis'], RDFS.comment, Literal(
    "The Coordinate System's Z axis vector.", lang="en")))

#Assembly.has_instance
g.add((SSO['has_instance'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_instance'], RDFS.domain, SSO.Assembly))
g.add((SSO['has_instance'], RDFS.range, SSO.Instance))
g.add((SSO['has_instance'], RDFS.label, Literal("has instance", lang="en")))
g.add((SSO['has_instance'], RDFS.comment, Literal(
    "Links an Assembly to one of its Instances.", lang="en")))

#Instance.referenced_object
g.add((SSO['referenced_object'], RDF.type, OWL.ObjectProperty))
g.add((SSO['referenced_object'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['referenced_object'], RDFS.domain, SSO.Instance))
g.add((SSO['referenced_object'], RDFS.range, SSO.Object))
g.add((SSO['referenced_object'], RDFS.label, Literal("references object", lang="en")))
g.add((SSO['referenced_object'], RDFS.comment, Literal(
    "Links an Instance to the Object it places within the Assembly.", lang="en")))

#Instance.has_nset
g.add((SSO['has_nset'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_nset'], RDFS.domain, SSO.Instance))
g.add((SSO['has_nset'], RDFS.range, SSO.Nset))
g.add((SSO['has_nset'], RDFS.label, Literal("has node set", lang="en")))
g.add((SSO['has_nset'], RDFS.comment, Literal(
    "Links an Instance to one of its Node Sets.", lang="en")))

#Instance.has_elset
g.add((SSO['has_elset'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_elset'], RDFS.domain, SSO.Instance))
g.add((SSO['has_elset'], RDFS.range, SSO.Elset))
g.add((SSO['has_elset'], RDFS.label, Literal("has element set", lang="en")))
g.add((SSO['has_elset'], RDFS.comment, Literal(
    "Links an Instance to one of its Element Sets.", lang="en")))

#Mesh.has_node / Nset.has_node / Element.has_node (shared: Mesh, Nset and
#Element are all unrelated classes that reference Node individuals, so no
#domain restriction — node ordering is not preserved)
g.add((SSO['has_node'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_node'], RDFS.range, SSO.Node))
g.add((SSO['has_node'], RDFS.label, Literal("has node", lang="en")))
g.add((SSO['has_node'], RDFS.comment, Literal(
    "Links a Mesh, Node Set, or Element to a Node it contains or connects "
    "to. Domain is intentionally open; node ordering is not preserved.", lang="en")))

#Mesh.has_element / Elset.has_element (shared, same reasoning as has_node)
g.add((SSO['has_element'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_element'], RDFS.range, SSO.Element))
g.add((SSO['has_element'], RDFS.label, Literal("has element", lang="en")))
g.add((SSO['has_element'], RDFS.comment, Literal(
    "Links a Mesh or Element Set to an Element it contains. Domain is "
    "intentionally open.", lang="en")))

#Element.element_material
g.add((SSO['element_material'], RDF.type, OWL.ObjectProperty))
g.add((SSO['element_material'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['element_material'], RDFS.domain, SSO.Element))
g.add((SSO['element_material'], RDFS.range, SSO.Material))
g.add((SSO['element_material'], RDFS.label, Literal("element material", lang="en")))
g.add((SSO['element_material'], RDFS.comment, Literal(
    "Links an Element to the Material assigned to it.", lang="en")))

#Element.element_section
g.add((SSO['element_section'], RDF.type, OWL.ObjectProperty))
g.add((SSO['element_section'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['element_section'], RDFS.domain, SSO.Element))
g.add((SSO['element_section'], RDFS.range, SSO.Section))
g.add((SSO['element_section'], RDFS.label, Literal("element section", lang="en")))
g.add((SSO['element_section'], RDFS.comment, Literal(
    "Links an Element to the Section assigned to it.", lang="en")))

#Material.has_elastic_behaviour
g.add((SSO['has_elastic_behaviour'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_elastic_behaviour'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_elastic_behaviour'], RDFS.domain, SSO.Material))
g.add((SSO['has_elastic_behaviour'], RDFS.range, SSO.ElasticBehaviour))
g.add((SSO['has_elastic_behaviour'], RDFS.label, Literal("has elastic behaviour", lang="en")))
g.add((SSO['has_elastic_behaviour'], RDFS.comment, Literal(
    "Links a Material to its Elastic Behaviour.", lang="en")))

#Material.has_plastic_behaviour
g.add((SSO['has_plastic_behaviour'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_plastic_behaviour'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_plastic_behaviour'], RDFS.domain, SSO.Material))
g.add((SSO['has_plastic_behaviour'], RDFS.range, SSO.PlasticBehaviour))
g.add((SSO['has_plastic_behaviour'], RDFS.label, Literal("has plastic behaviour", lang="en")))
g.add((SSO['has_plastic_behaviour'], RDFS.comment, Literal(
    "Links a Material to its Plastic Behaviour, when the material has one.", lang="en")))

#Section.section_material
g.add((SSO['section_material'], RDF.type, OWL.ObjectProperty))
g.add((SSO['section_material'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['section_material'], RDFS.domain, SSO.Section))
g.add((SSO['section_material'], RDFS.range, SSO.Material))
g.add((SSO['section_material'], RDFS.label, Literal("section material", lang="en")))
g.add((SSO['section_material'], RDFS.comment, Literal(
    "Links a Section to the default Material it uses.", lang="en")))

#BeamSection.orientation
g.add((SSO['orientation'], RDF.type, OWL.ObjectProperty))
g.add((SSO['orientation'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['orientation'], RDFS.domain, SSO.BeamSection))
g.add((SSO['orientation'], RDFS.range, SSO.Vector3D))
g.add((SSO['orientation'], RDFS.label, Literal("orientation", lang="en")))
g.add((SSO['orientation'], RDFS.comment, Literal(
    "Links a Beam Section to the vector defining the local orientation of "
    "its cross-section along the beam axis.", lang="en")))

#BeamSection.has_cross_section (always expected to be present, matching the
#now-required cross_section field in osam.py)
g.add((SSO['has_cross_section'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_cross_section'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_cross_section'], RDFS.domain, SSO.BeamSection))
g.add((SSO['has_cross_section'], RDFS.range, SSO.CrossSectionProfile))
g.add((SSO['has_cross_section'], RDFS.label, Literal("has cross-section", lang="en")))
g.add((SSO['has_cross_section'], RDFS.comment, Literal(
    "Links a Beam Section to its Cross-Section Profile; always expected to "
    "be present.", lang="en")))

#LoadCase.selfWeight
g.add((SSO['selfWeight'], RDF.type, OWL.ObjectProperty))
g.add((SSO['selfWeight'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['selfWeight'], RDFS.domain, SSO.LoadCase))
g.add((SSO['selfWeight'], RDFS.range, SSO.Vector3D))
g.add((SSO['selfWeight'], RDFS.label, Literal("self-weight", lang="en")))
g.add((SSO['selfWeight'], RDFS.comment, Literal(
    "Links a Load Case to the vector defining the direction and magnitude of "
    "the self-weight it applies.", lang="en")))

#Load.applied_to / BoundaryCondition.applied_to (shared: Load and
#BoundaryCondition are unrelated classes, so no domain restriction)
g.add((SSO['applied_to'], RDF.type, OWL.ObjectProperty))
g.add((SSO['applied_to'], RDFS.range, SSO.Instance))
g.add((SSO['applied_to'], RDFS.label, Literal("applied to", lang="en")))
g.add((SSO['applied_to'], RDFS.comment, Literal(
    "Links a Load or Boundary Condition to the Instance(s) it is scoped to. "
    "Domain is intentionally open.", lang="en")))

#Load.in_loadCase (Load.caseName in OSAM is a field on the load itself,
#pointing at its LoadCase — the accurate direction for this relationship)
g.add((SSO['in_loadCase'], RDF.type, OWL.ObjectProperty))
g.add((SSO['in_loadCase'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['in_loadCase'], RDFS.domain, SSO.Load))
g.add((SSO['in_loadCase'], RDFS.range, SSO.LoadCase))
g.add((SSO['in_loadCase'], RDFS.label, Literal("in load case", lang="en")))
g.add((SSO['in_loadCase'], RDFS.comment, Literal(
    "Links a Load to the Load Case it belongs to.", lang="en")))

#PointLoad.nset / BoundaryCondition.nset (shared: PointLoad and
#BoundaryCondition are unrelated classes, so no domain restriction)
g.add((SSO['nset'], RDF.type, OWL.ObjectProperty))
g.add((SSO['nset'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['nset'], RDFS.range, SSO.Nset))
g.add((SSO['nset'], RDFS.label, Literal("node set", lang="en")))
g.add((SSO['nset'], RDFS.comment, Literal(
    "Links a Point Load or Boundary Condition to the Node Set it acts on. "
    "Domain is intentionally open.", lang="en")))

#DistributedLoad.elset / SurfaceLoad.elset (shared: sibling subclasses of
#Load, so domain is the common parent)
g.add((SSO['elset'], RDF.type, OWL.ObjectProperty))
g.add((SSO['elset'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['elset'], RDFS.domain, SSO.Load))
g.add((SSO['elset'], RDFS.range, SSO.Elset))
g.add((SSO['elset'], RDFS.label, Literal("element set", lang="en")))
g.add((SSO['elset'], RDFS.comment, Literal(
    "Links a Distributed Load or Surface Load to the Element Set it acts "
    "on.", lang="en")))


# Save rdf ontology
g.serialize(destination= save_path + '.ttl', format ='turtle')


##########################################################
#                   Coverage report                       #
##########################################################

def _has(term, predicate):
    return any(True for _ in g.triples((term, predicate, None)))


def _annotation_coverage(rdf_type):
    terms = set(g.subjects(RDF.type, rdf_type))
    complete = {t for t in terms if _has(t, RDFS.label) and _has(t, RDFS.comment)}
    missing = terms - complete
    return terms, complete, missing


classes, classes_ok, classes_missing = _annotation_coverage(OWL.Class)
dprops, dprops_ok, dprops_missing = _annotation_coverage(OWL.DatatypeProperty)
oprops, oprops_ok, oprops_missing = _annotation_coverage(OWL.ObjectProperty)

print(f"Classes annotated: {len(classes_ok)}/{len(classes)}")
print(f"Datatype properties annotated: {len(dprops_ok)}/{len(dprops)}")
print(f"Object properties annotated: {len(oprops_ok)}/{len(oprops)}")

missing_all = classes_missing | dprops_missing | oprops_missing
if missing_all:
    print("Missing rdfs:label and/or rdfs:comment:")
    for term in sorted(missing_all):
        print(f"  {term}")
else:
    print("All classes and properties have both rdfs:label and rdfs:comment.")
