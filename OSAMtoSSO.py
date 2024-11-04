import json as JSON
import pathlib
from rdflib import Graph, Namespace, Literal, URIRef

# Define the path to your JSON file
file_path = 'FootbridgeSA.json'  # Adjust the path if necessary

#Load the conversion map from IFC to RDF
script_dir = pathlib.Path(__file__).parent
osam_file = (script_dir / 'FootbridgeSA.json').resolve()
with open(osam_file, 'r',encoding='utf-8') as fp:
    osam =JSON.load(fp)

#Instance reference
base_ref = "http://www.upclabmodelsdigitals.org/Models/OSAM/"
inst_base_ref = base_ref
inst_ref = URIRef(inst_base_ref)

#SSO reference
sso_base_ref = base_ref + "SSO#"
sso_ref =  URIRef(sso_base_ref)

#IFC-SSO reference
ifcsso_base_ref = base_ref + "IFCSSO#"
ifcsso_ref =  URIRef(ifcsso_base_ref)

#Get the structural analysis data
SA_name = osam['name']
SA_instance = URIRef(sso_base_ref+"structuralAnalysisModel")
SA_id = osam['id']
SA_ref = URIRef(base_ref + SA_name)

# Instantiate  empty  graph
g  = Graph()

# Create a namespaces
SSO = Namespace(sso_ref)
IFCSSO = Namespace(ifcsso_ref)
INST = Namespace(inst_ref)
CC = Namespace('http://creativecommons.org/ns#')
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

# Bind your custom prefix
g.bind("sso", SSO)
g.bind("ifcsso", IFCSSO)
g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('owl', OWL)
g.bind('xsd', XSD)
g.bind('cc', CC)
g.bind("osam_simulation", INST)

#add ontology header triples
g.add((sso_ref, RDF.type, OWL.Ontology))

#Add StructuralAnalysisModel entity
sa_uri = INST[SA_name]
osamJson = "as_OSAM-json"
g.add((sa_uri, RDF.type, SSO.StructuralAnalysisModel))
g.add((sa_uri, SSO.name, Literal(SA_name, datatype=XSD.string)))
g.add((sa_uri, SSO.id, Literal(SA_id, datatype=XSD.string)))
g.add((sa_uri, SSO["as_OSAM-json"], Literal("OSAM-model-uri", datatype=XSD.string)))

#add Materials
for mat in osam['materials']:
    mat_name = mat['name']
    mat_uri = INST[mat_name]
    g.add((mat_uri, RDF.type, SSO.Material))
    g.add((mat_uri, SSO.material_name, Literal(mat_name, datatype=XSD.string)))
    g.add((sa_uri, SSO.has_material, mat_uri))
    if mat['elastic'] is None:
        g.add((mat_uri, SSO.elastic, Literal(False, datatype=XSD.boolean)))
    else:
        g.add((mat_uri, SSO.elastic, Literal(True, datatype=XSD.boolean)))
    if mat['plastic'] is None:
        g.add((mat_uri, SSO.plastic, Literal(False, datatype=XSD.boolean)))
    else:
        g.add((mat_uri, SSO.plastic, Literal(True, datatype=XSD.boolean)))

#add Sections
sections = osam['sections']
for sec in sections:
    sec_name = sec['name']
    sec_type = sec['section_type']
    sec_uri = INST[sec_name]
    g.add((sec_uri, RDF.type, SSO.Section))
    g.add((sec_uri, SSO.section_name, Literal(sec_name, datatype=XSD.string)))
    g.add((sec_uri, SSO.section_type, Literal(sec_type, datatype=XSD.string)))
    g.add((sa_uri, SSO.has_section, sec_uri))

#add Objects
objects = osam['objects']
for obj in objects:
    obj_name = obj['name']
    obj_uri = INST[obj_name]
    g.add((obj_uri, RDF.type, SSO.Object))
    g.add((obj_uri, SSO.object_name, Literal(obj_name, datatype=XSD.string)))
    g.add((sa_uri, SSO.has_object, obj_uri))
    #add the mesh of the object
    mesh = obj['mesh']
    mesh_uri = INST[obj_name + '_Mesh']
    mesh_nodes = mesh['node_count']
    g.add((mesh_uri, RDF.type, SSO.Mesh))
    g.add((mesh_uri, SSO.nodes, Literal(mesh_nodes, datatype=XSD.integer)))
    g.add((obj_uri, SSO.has_mesh, mesh_uri))
    #add the elements of the object
    elements = mesh['elements']
    for elem in elements:
        elem_id = elem['id']
        elem_uri = INST['Element_'+str(elem_id)]
        g.add((elem_uri, RDF.type, SSO.Element))
        if elem['type'] == 'SHELL':
            g.add((elem_uri, RDF.type, SSO.ShellElement))
        elif elem['type'] == 'BEAM':
            g.add((elem_uri, RDF.type, SSO.BeamElement))
        elif elem['type'] == 'SOLID':
            g.add((elem_uri, RDF.type, SSO.SolidElement))
        elif elem['type'] == 'MEMBRANE':
            g.add((elem_uri, RDF.type, SSO.MembraneElement))
        elif elem['type'] == 'TRUSS':
            g.add((elem_uri, RDF.type, SSO.TrussElement))
        node_count = elem['node_count']
        g.add((elem_uri, SSO.node_count, Literal(node_count, datatype=XSD.integer)))
        face_count = elem['face_count']
        g.add((elem_uri, SSO.face_count, Literal(face_count, datatype=XSD.integer)))
        dofs = len(elem['dofs'])
        g.add((elem_uri, SSO.dofs, Literal(dofs, datatype=XSD.integer)))
        g.add((mesh_uri, SSO.has_element, elem_uri))
        #Find the section and add the element_section
        elem_sec_id = elem['section']
        elem_sec = None
        for sec in sections:
            if sec['id'] == elem_sec_id:
                elem_sec = sec['name']
        sec_uri = None
        for s, p, o in g.triples((None, SSO.section_name, Literal(elem_sec, datatype=XSD.string))):
            sec_uri = s
        g.add((elem_uri, SSO.element_section, sec_uri))
        #Find the material and add the element_material
        elem_mat = elem['material']
        mat_uri = None
        for s, p, o in g.triples((None, SSO.material_name, Literal(elem_mat, datatype=XSD.string))):
            mat_uri = s
        g.add((elem_uri, SSO.element_material, mat_uri))

#add the Assembly
ass_name = osam['assembly']['name']
ass_uri = INST[ass_name]
g.add((ass_uri, RDF.type, SSO.Assembly))
g.add((ass_uri, SSO.assembly_name, Literal(ass_name, datatype=XSD.string)))
g.add((sa_uri, SSO.has_assembly, ass_uri))

#add Instances
instances = osam['assembly']['instances']
for inst in instances:
    inst_name = inst['name']
    inst_uri = INST[inst_name]
    g.add((inst_uri, RDF.type, SSO.Instance))
    g.add((inst_uri, SSO.instance_name, Literal(inst_name, datatype=XSD.string)))
    g.add((ass_uri,SSO.has_instance,inst_uri))
    #Query the referenced object uri and add referenced_object
    inst_ref_obj_id = inst['referenced_object']
    inst_ref_obj_name = None
    for obj in objects:
        if inst_ref_obj_id == obj['id']:
            inst_ref_obj_name = obj['name']
        inst_ref_obj_uri = None
        for s, p, o in g.triples((None, SSO.object_name, Literal(inst_ref_obj_name , datatype=XSD.string))):
                inst_ref_obj_uri = s
        g.add((inst_uri, SSO.referenced_object, inst_ref_obj_uri))

#add Boundary Conditions
boundCondi = osam['bc']
bcCounter = 1
for bc in boundCondi:
    bc_uri = INST["bc_"+str(bcCounter)]
    bcCounter += 1
    g.add((bc_uri, RDF.type, SSO.BoundaryCondition))
    g.add((sa_uri, SSO.has_boundary_condition, bc_uri))
    #Query the bc instances names and add applied_to
    bc_instas = bc['instances']
    bc_inst_name = None
    for bc_inst in bc_instas:
        for inst in instances:
            if bc_inst == inst['id']:
                bc_inst_name = inst['name']
        bc_inst_uri = None
        for s, p, o in g.triples((None, SSO.instance_name, Literal(bc_inst_name, datatype=XSD.string))):
            bc_inst_uri = s
        g.add((bc_uri, SSO.applied_to, bc_inst_uri))

#add Load Case
loadCases = osam['loadCases']
for loadCase in loadCases:
    loadCase_name = loadCase['name']
    loadCase_type = loadCase['type']
    loadCase_uri = INST[loadCase_name]
    g.add((loadCase_uri, RDF.type, SSO.LoadCase))
    g.add((loadCase_uri, SSO.loadCase_name, Literal(loadCase_name, datatype=XSD.string)))
    g.add((loadCase_uri, SSO.loadCase_type, Literal(loadCase_type, datatype=XSD.string)))
    g.add((sa_uri, SSO.has_loadCase, loadCase_uri))

#add Loads
loads = osam['loads']
loadsCounter = 1
for load in loads:
    load_uri = INST["load_"+str(loadsCounter)]
    load_type = load['type']
    load_loadCase = load['caseName']
    loadsCounter += 1
    g.add((load_uri, RDF.type, SSO.Load))
    g.add((load_uri, SSO.load_type, Literal(load_type, datatype=XSD.string)))
    g.add((sa_uri, SSO.has_load, load_uri))
    #Query the load case and add has_load
    load_case_uri = None
    for s, p, o in g.triples((None, SSO.loadCase_name, Literal(load_loadCase, datatype=XSD.string))):
            load_case_uri = s
    g.add((load_case_uri, SSO.has_load, load_uri))
    #Query the loads instances names and add applied_to
    load_instas = load['instances']
    load_inst_name = None
    for load_inst in load_instas:
        for inst in instances:
            if load_inst == inst['id']:
                load_inst_name = inst['name']
        load_inst_uri = None
        for s, p, o in g.triples((None, SSO.instance_name, Literal(load_inst_name, datatype=XSD.string))):
            load_inst_uri = s
        g.add((load_uri, SSO.applied_to, load_inst_uri))

# Save the graph to a file
g.serialize(destination='ontology.ttl', format='turtle')
