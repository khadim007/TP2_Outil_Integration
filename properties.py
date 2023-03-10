from rdflib import Graph

# Chargement des deux fichiers Turtle
graph1 = Graph().parse("source.ttl", format="turtle")
graph2 = Graph().parse("target.ttl", format="turtle")

# Extraction des propriétés des deux graphes
properties_graph1 = set()
for s, p, o in graph1:
    properties_graph1.add(str(p))
    
properties_graph2 = set()
for s, p, o in graph2:
    properties_graph2.add(str(p))

# Trouver les propriétés communes aux deux graphes
common_properties = properties_graph1.intersection(properties_graph2)
print("Propriétés communes : ")
print(common_properties)

# Trouver les propriétés uniques à chaque graphe
unique_properties_graph1 = properties_graph1 - properties_graph2
unique_properties_graph2 = properties_graph2 - properties_graph1
print("Propriétés uniques au graphe 1 : ")
print(unique_properties_graph1)
print("Propriétés uniques au graphe 2 : ")
print(unique_properties_graph2)

"""
Resultat:

Propriétés communes : 
    {'http://erlangen-crm.org/current/P3_has_note', 
    'http://data.doremus.org/ontology#U12_has_genre', 
    'http://data.doremus.org/ontology#U16_has_catalogue_statement', 
    'http://data.doremus.org/ontology#U4_had_princeps_publication', 
    'http://erlangen-crm.org/efrbroo/R40_has_representative_expression', 
    'http://erlangen-crm.org/efrbroo/R25_performed', 
    'http://erlangen-crm.org/efrbroo/R9_is_realised_in', 
    'http://data.doremus.org/ontology#U13_has_casting', 
    'http://data.doremus.org/ontology#U17_has_opus_statement', 
    'http://erlangen-crm.org/efrbroo/R50_assigned_to', 
    'http://erlangen-crm.org/current/P9_consists_of', 
    'http://data.doremus.org/ontology#U40_has_catalogue_name', 
    'http://erlangen-crm.org/current/P165_incorporates', 
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 
    'http://data.doremus.org/ontology#U5_had_premiere', 
    'http://data.doremus.org/ontology#U11_has_key', 
    'http://erlangen-crm.org/current/P1_is_identified_by', 
    'http://erlangen-crm.org/efrbroo/R19_created_a_realisation_of', 
    'http://data.doremus.org/ontology#U42_has_opus_number', 
    'http://erlangen-crm.org/efrbroo/R24_created', 
    'http://erlangen-crm.org/efrbroo/R17_created', 
    'http://erlangen-crm.org/current/P82_at_some_time_within', 
    'http://erlangen-crm.org/current/P102_has_title', 
    'http://erlangen-crm.org/efrbroo/R51_assigned', 
    'http://erlangen-crm.org/efrbroo/R10_has_member', 
    'http://erlangen-crm.org/current/P14_carried_out_by', 
    'http://erlangen-crm.org/efrbroo/R3_is_realised_in', 
    'http://data.doremus.org/ontology#U31_had_function_of_type', 
    'http://data.doremus.org/ontology#U43_has_opus_subnumber', 
    'http://erlangen-crm.org/current/P4_has_time-span', 
    'http://data.doremus.org/ontology#U10_has_order_number', 
    'http://erlangen-crm.org/efrbroo/R44_carried_out_by', 
    'http://data.doremus.org/ontology#U41_has_catalogue_number'}

Propriétés uniques au graphe 1 : 
   {'http://erlangen-crm.org/current/P10_falls_within'}

Propriétés uniques au graphe 2 : 
   {'http://erlangen-crm.org/current/P81_ongoing_throughout', 
    'http://data.doremus.org/ontology#U23_has_casting_detail', 
    'http://erlangen-crm.org/current/P67_refers_to', 
    'http://data.doremus.org/ontology#U44_has_dedication_statement', 
    'http://data.doremus.org/ontology#U2_foresees_use_of_medium_of_performance_of_type'}

"""