from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, VANN, DCTERMS, XSD

ref =  URIRef("http://www.example.org/ontologies/SSO#")
save_path =  'test_ontology'

# Instantiate  empty  graph for the ontology
g  = Graph()

# Create a namespaces
SSO = Namespace(ref)
CC = Namespace('http://creativecommons.org/ns#')

# Bind your custom prefix
g.bind("sso", SSO)
g.bind('rdf',RDF)
g.bind('rdfs',RDFS)
g.bind('owl', OWL)
g.bind('xsd', XSD)
g.bind('cc', CC)

#add ontology header triples
g.add((ref, RDF.type, OWL.Ontology))
g.add((ref, DCTERMS.creator, Literal('Carlos Ramonell Cazador (carlos.ramonell@upc.edu)')))
g.add((ref, DCTERMS.contributor, Literal('Héctor Posada Cárcamo (hector.posada@upc.edu)')))
g.add((ref, DCTERMS.date, Literal('2024/01/04')))
g.add((ref, DCTERMS.title, Literal('SSO')))
g.add((ref, DCTERMS.description, Literal("ontology containing the description of structural simulation models (openFEM)")))
g.add((ref, DCTERMS.format, Literal('ttl')))
g.add((ref, DCTERMS.identifier, Literal('SSO')))
g.add((ref, DCTERMS.language, Literal('en')))
g.add((ref, VANN.preferredNamespacePrefix, Literal('sso')))
g.add((ref, VANN.preferredNamespaceUri, Literal(ref)))
g.add((ref, CC.license, Literal('http://creativecommons.org/licenses/by/3.0/')))


##########################################################
#                       classes                          #
##########################################################

g.add((SSO['StructuralAnalysisModel'], RDF.type, OWL.Class))

g.add((SSO['Object'], RDF.type, OWL.Class))

g.add((SSO['Assembly'], RDF.type, OWL.Class))

g.add((SSO['Instance'], RDF.type, OWL.Class))

g.add((SSO['Material'], RDF.type, OWL.Class))

g.add((SSO['Section'], RDF.type, OWL.Class))

g.add((SSO['Mesh'], RDF.type, OWL.Class))

g.add((SSO['Element'], RDF.type, OWL.Class))

g.add((SSO['SolidElement'], RDF.type, OWL.Class))
g.add((SSO['SolidElement'], RDFS.subClassOf, SSO.Element))

g.add((SSO['ShellElement'], RDF.type, OWL.Class))
g.add((SSO['ShellElement'], RDFS.subClassOf, SSO.Element))

g.add((SSO['BeamElement'], RDF.type, OWL.Class))
g.add((SSO['BeamElement'], RDFS.subClassOf, SSO.Element))

g.add((SSO['MembraneElement'], RDF.type, OWL.Class))
g.add((SSO['MembraneElement'], RDFS.subClassOf, SSO.Element))

g.add((SSO['TrussElement'], RDF.type, OWL.Class))
g.add((SSO['TrussElement'], RDFS.subClassOf, SSO.Element))

g.add((SSO['Load'], RDF.type, OWL.Class))

g.add((SSO['BoundaryCondition'], RDF.type, OWL.Class))


##########################################################
#                  Datatype Porperties                   #
##########################################################
#StructuralAnalysisModel.id
g.add((SSO['id'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['id'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['id'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['id'], RDFS.range, XSD.string))

#StructuralAnalysisModel.format
g.add((SSO['id'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['id'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['id'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['id'], RDFS.range, XSD.string))

#StructuralAnalysisModel.as_openFEM-json
g.add((SSO['as_openFEM-json'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['as_openFEM-json'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['as_openFEM-json'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['as_openFEM-json'], RDFS.range, XSD.string))
g.add((SSO['as_openFEM-json'], RDFS.range, XSD.anyURI))

#StructuralAnalysisModel.as_abaqus-inp
g.add((SSO['as_abaqus-inp'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['as_abaqus-inp'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['as_abaqus-inp'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['as_abaqus-inp'], RDFS.range, XSD.string))
g.add((SSO['as_abaqus-inp'], RDFS.range, XSD.anyURI))

#StructuralAnalysisModel.creation_date
g.add((SSO['creation_date'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['creation_date'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['creation_date'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['creation_date'], RDFS.range, XSD.dateTimeStamp))
g.add((SSO['creation_date'], RDFS.range, XSD.dateTime))

#Object.name
g.add((SSO['object_name'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['object_name'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['object_name'], RDFS.domain, SSO.Object))
g.add((SSO['object_name'], RDFS.range, XSD.string))

#Assembly.name
g.add((SSO['assembly_name'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['assembly_name'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['assembly_name'], RDFS.domain, SSO.Assembly))
g.add((SSO['assembly_name'], RDFS.range, XSD.string))

#Instance.name
g.add((SSO['instance_name'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['instance_name'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['instance_name'], RDFS.domain, SSO.Instance))
g.add((SSO['instance_name'], RDFS.range, XSD.string))

#Mesh.nodes
g.add((SSO['nodes'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['nodes'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['nodes'], RDFS.domain, SSO.Mesh))
g.add((SSO['nodes'], RDFS.range, XSD.integer))

#Section.name
g.add((SSO['section_name'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['section_name'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['section_name'], RDFS.domain, SSO.Section))
g.add((SSO['section_name'], RDFS.range, XSD.string))


#Material.name
g.add((SSO['material_name'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['material_name'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['material_name'], RDFS.domain, SSO.Material))
g.add((SSO['material_name'], RDFS.range, XSD.string))

#Material.elastic
g.add((SSO['elastic'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['elastic'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['elastic'], RDFS.domain, SSO.Material))
g.add((SSO['elastic'], RDFS.range, XSD.boolean))

#Material.plastic
g.add((SSO['plastic'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['plastic'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['plastic'], RDFS.domain, SSO.Material))
g.add((SSO['plastic'], RDFS.range, XSD.boolean))

#Element.node_count
g.add((SSO['node_count'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['node_count'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['node_count'], RDFS.domain, SSO.Element))
g.add((SSO['node_count'], RDFS.range, XSD.integer))

#Element.face_count
g.add((SSO['face_count'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['face_count'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['face_count'], RDFS.domain, SSO.Element))
g.add((SSO['face_count'], RDFS.range, XSD.integer))

#Element.dofs
g.add((SSO['dofs'], RDF.type, OWL.DatatypeProperty))
g.add((SSO['dofs'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['dofs'], RDFS.domain, SSO.Element))
g.add((SSO['dofs'], RDFS.range, XSD.integer))


##########################################################
#                   ObjectType Porperties                    #
##########################################################

#StructuralAnalysisModel.has_object
g.add((SSO['has_object'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_object'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_object'], RDFS.range, SSO.Object))

#StructuralAnalysisModel.has_assembly
g.add((SSO['has_assembly'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_assembly'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_assembly'], RDFS.range, SSO.Assembly))

#StructuralAnalysisModel.has_material
g.add((SSO['has_material'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_material'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_material'], RDFS.range, SSO.Material))

#StructuralAnalysisModel.has_section
g.add((SSO['has_section'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_section'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_section'], RDFS.range, SSO.Section))

#StructuralAnalysisModel.has_load
g.add((SSO['has_load'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_load'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_load'], RDFS.range, SSO.Load))

#StructuralAnalysisModel.has_boundary_condition
g.add((SSO['has_boundary_condition'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_boundary_condition'], RDFS.domain, SSO.StructuralAnalysisModel))
g.add((SSO['has_boundary_condition'], RDFS.range, SSO.BoundaryCondition))

#Object.has_mesh
g.add((SSO['has_mesh'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_mesh'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['has_mesh'], RDFS.domain, SSO.Object))
g.add((SSO['has_mesh'], RDFS.range, SSO.Mesh))

#Assembly.has_instance
g.add((SSO['has_instance'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_instance'], RDFS.domain, SSO.Assembly))
g.add((SSO['has_instance'], RDFS.range, SSO.Instance))

#Instance.referenced_object
g.add((SSO['referenced_object'], RDF.type, OWL.ObjectProperty))
g.add((SSO['referenced_object'], RDF.type, OWL.FunctionalProperty))
g.add((SSO['referenced_object'], RDFS.domain, SSO.Instance))
g.add((SSO['referenced_object'], RDFS.range, SSO.Object))

#Mesh.has_element
g.add((SSO['has_element'], RDF.type, OWL.ObjectProperty))
g.add((SSO['has_element'], RDFS.domain, SSO.Mesh))
g.add((SSO['has_element'], RDFS.range, SSO.Element))

#Section.section_material
g.add((SSO['section_material'], RDF.type, OWL.ObjectProperty))
g.add((SSO['section_material'], RDFS.domain, SSO.Section))
g.add((SSO['section_material'], RDFS.range, SSO.Material))

#Element.element_section
g.add((SSO['element_section'], RDF.type, OWL.ObjectProperty))
g.add((SSO['element_section'], RDFS.domain, SSO.Element))
g.add((SSO['element_section'], RDFS.range, SSO.Section))

#Load.applied_to
g.add((SSO['applied_to'], RDF.type, OWL.ObjectProperty))
g.add((SSO['applied_to'], RDFS.domain, SSO.Load))
g.add((SSO['applied_to'], RDFS.range, SSO.Instance))

#BoundaryCondition.applied_to
g.add((SSO['applied_to'], RDF.type, OWL.ObjectProperty))
g.add((SSO['applied_to'], RDFS.domain, SSO.BoundaryCondition))
g.add((SSO['applied_to'], RDFS.range, SSO.Instance))


# Save rdf ontology
g.serialize(destination= save_path + '.ttl', format ='turtle')