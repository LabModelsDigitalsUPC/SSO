from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, VANN, DCTERMS, XSD

openFEM_ref =  URIRef("http://www.carlos.test/ontologies/SSO#")
IFC_ref = URIRef("http://www.carlos.test/ontologies/IFC4X3/")
IFC_openFEM_ref = URIRef("http://www.carlos.test/ontologies/IFC-SSO#")
save_path =  'test_ontology_link'

# Instantiate  empty  graph for the ontology
g  = Graph()

# Create a namespaces
SSO = Namespace(openFEM_ref)
IFC = Namespace(IFC_ref)
LINK = Namespace(IFC_openFEM_ref)
CC = Namespace('http://creativecommons.org/ns#')

# Bind your custom prefix
g.bind("sso", SSO)
g.bind('ifc', IFC)
g.bind('link', LINK)
g.bind('rdf',RDF)
g.bind('rdfs',RDFS)
g.bind('owl', OWL)
g.bind('xsd', XSD)
g.bind('cc', CC)

g.add((SSO['StructuralAnalysisModel'], RDF.type, OWL.Class))

g.add((IFC['IfcElement'], RDF.type, OWL.Class))

g.add((LINK['referenced_in_sam'], RDF.type, OWL.ObjectProperty))
g.add((LINK['referenced_in_sam'], RDF.type, OWL.FunctionalProperty))
g.add((LINK['referenced_in_sam'], RDFS.domain, OWL.Thing))
g.add((LINK['referenced_in_sam'], RDFS.range, SSO['StructuralAnalysisModel']))

# Save rdf ontology
g.serialize(destination= save_path + '.ttl', format ='turtle')