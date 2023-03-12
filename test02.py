from rdflib import *
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
import warnings
import py_stringmatching as psm

# Chargement du graphe RDF
graph_ref = Graph().parse("refDHT.rdf", format="xml")
graph1 = Graph().parse("source.ttl", format="turtle")
graph2 = Graph().parse("target.ttl", format="turtle")

propriete_clef_1 = set()
propriete_titre_1 = set()
propriete_note_1 = set()
propriete_opus_1 = set()
propriete_compositeur_1 = set()
propriete_genre_1 = set()

propriete_clef_2 = set()
propriete_titre_2 = set()
propriete_note_2 = set()
propriete_opus_2 = set()
propriete_compositeur_2 = set()
propriete_genre_2 = set()

req_clef = """ 
    PREFIX mus: <http://data.doremus.org/ontology#>
    SELECT ?expression ?clef
    WHERE{
        ?expression mus:U11_has_key ?clef.
        FILTER(isIRI(?clef)).
    }"""

req_note = """ 
    PREFIX ecrm: <http://erlangen-crm.org/current/>
    SELECT ?expression ?note
    WHERE{
        ?expression ecrm:P3_has_note ?note.
    }"""

req_opus = """ 
    PREFIX mus: <http://data.doremus.org/ontology#>
    SELECT ?expression ?opus
    WHERE{
        ?expression mus:U17_has_opus_statement / mus:U42_has_opus_number ?opus.
    }"""

req_compositeur = """
    PREFIX ecrm: <http://erlangen-crm.org/current/>
    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
    SELECT ?expression ?compositeur
    WHERE{
        ?expression a efrbroo:F22_Self-Contained_Expression .
        ?expCreation efrbroo:R17_created ?expression ;
        ecrm:P9_consists_of / ecrm:P14_carried_out_by ?compositeur ;
    }"""

req_titre = """
    PREFIX ecrm: <http://erlangen-crm.org/current/>
    SELECT ?expression ?title
    WHERE {
        ?expression ecrm:P102_has_title ?title .
    }"""

req_genre = """
    PREFIX mus: <http://data.doremus.org/ontology#>
    SELECT ?expression ?genre
    WHERE {
        ?expression mus:U12_has_genre ?genre.
        FILTER (isIRI(?genre))
    }"""

res_req_clef_1 = graph1.query(req_clef)
for row in res_req_clef_1:
    propriete_clef_1.add(str(row[0]))

res_req_clef_2 = graph2.query(req_clef)
for row in res_req_clef_2:
    propriete_clef_2.add(str(row[0]))

res_req_titre_1 = graph1.query(req_titre)
for row in res_req_titre_1:
    propriete_titre_1.add(str(row[0]))

res_req_titre_2 = graph2.query(req_titre)
for row in res_req_titre_2:
    propriete_titre_2.add(str(row[0]))

res_req_opus_1 = graph1.query(req_opus)
for row in res_req_opus_1:
    propriete_opus_1.add(str(row[0]))

res_req_opus_2 = graph2.query(req_opus)
for row in res_req_opus_2:
    propriete_opus_2.add(str(row[0]))

res_req_note_1 = graph1.query(req_note)
for row in res_req_note_1:
    propriete_note_1.add(str(row[0]))

res_req_note_2 = graph2.query(req_note)
for row in res_req_note_2:
    propriete_note_2.add(str(row[0]))

res_req_compositeur_1 = graph1.query(req_compositeur)
for row in res_req_compositeur_1:
    propriete_compositeur_1.add(str(row[0]))

res_req_compositeur_2 = graph2.query(req_compositeur)
for row in res_req_compositeur_2:
    propriete_compositeur_2.add(str(row[0]))

res_req_genre_1 = graph1.query(req_genre)
for row in res_req_genre_1:
    propriete_genre_1.add(str(row[0]))

res_req_genre_2 = graph2.query(req_genre)
for row in res_req_genre_2:
    propriete_genre_2.add(str(row[0]))

"""
print("propriete_clef_1 = ",propriete_clef_1)
print("propriete_clef_2 = ",propriete_clef_2)

print("propriete_titre_1 = ",propriete_titre_1)
print("propriete_titre_2 = ",propriete_titre_2)

print("propriete_genre_1 = ",propriete_genre_1)
print("propriete_genre_2 = ",propriete_genre_2)

print("propriete_opus_1 = ",propriete_opus_1)
print("propriete_opus_2 = ",propriete_opus_2)

print("propriete_compositeur_1 = ",propriete_compositeur_1)
print("propriete_compositeur_2 = ",propriete_compositeur_2)

print("propriete_note_1 = ",propriete_note_1)
print("propriete_note_2 = ",propriete_note_2)
"""

# Définition des namespaces utilisés dans le fichier RDF
ALIGN = Namespace("http://knowledgeweb.semanticweb.org/heterogeneity/alignment")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# Récupération des paires e1 et e2 ayant une mesure de correspondance de 1.0
alignments = []
for s, p, o in graph_ref.triples((None, RDF.type, ALIGN.Cell)):
    e1 = str(graph_ref.value(s, ALIGN.entity1, None))
    e2 = str(graph_ref.value(s, ALIGN.entity2, None))
    measure = float(str(graph_ref.value(s, ALIGN.measure, None)))
    if measure == 1.0:
        alignments.append((e1, e2))

#print(alignments)

# On recupere tous les alignements par paroprietes 
alignements_clef = []
alignements_titre = []
alignements_genre = []
alignements_opus = []
alignements_compositeur = []
alignements_note = []


for e in propriete_clef_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_clef):
            alignements_clef.append(tuple)

for e in propriete_clef_2:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_clef):
            alignements_clef.append(tuple)

for e in propriete_titre_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_titre):
            alignements_titre.append(tuple)

for e in propriete_titre_2:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_titre):
            alignements_titre.append(tuple)

for e in propriete_genre_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_genre):
            alignements_genre.append(tuple)

for e in propriete_genre_2:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_genre):
            alignements_genre.append(tuple)

for e in propriete_opus_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_opus):
            alignements_opus.append(tuple)

for e in propriete_opus_2:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_opus):
            alignements_opus.append(tuple)

for e in propriete_compositeur_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_compositeur):
            alignements_compositeur.append(tuple)

for e in propriete_compositeur_2:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_compositeur):
            alignements_compositeur.append(tuple)

for e in propriete_note_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_note):
            alignements_note.append(tuple)

for e in propriete_note_1:
    for tuple in alignments:
        if (e in tuple) and (tuple not in alignements_note):
            alignements_note.append(tuple)


#print(alignements_titre)


def validation(fichier_res, proprietes):
    # Lire le fichier texte de la forme (e1, owl:SameAs, e2) et extraire les paires d'URI
    pairs = []
    with open(fichier_res, "r") as f:
        lines = f.read().strip().split('\n\n')
        for line in lines:
            e1, _, e2 = line.strip().split('\n')
            pairs.append((e1[1:-1], e2[1:-1]))
    
    print(pairs)
    
    nb_correspondances_clef = 0
    nb_correspondances_titre = 0
    nb_correspondances_opus = 0
    nb_correspondances_genre = 0
    nb_correspondances_note = 0
    nb_correspondances_compositeur = 0
    nb_correspondances = 0

    for propriete in proprietes:
        if (propriete == "clef"):
            for e1, e2 in pairs:
                if (e1, e2) in alignements_clef or (e2, e1) in alignements_clef:
                    nb_correspondances_clef += 1
            # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
            precision = nb_correspondances_clef / len(pairs)
            rappel = nb_correspondances_clef / len(alignements_clef)
            f_mesure = 2 * precision * rappel / (precision + rappel)

            print(precision)
            print(rappel)
            print(f_mesure)

        elif (propriete == "note"):
            for e1, e2 in pairs:
                if (e1, e2) in alignements_note or (e2, e1) in alignements_note:
                    nb_correspondances_note += 1
            # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
            precision = nb_correspondances_note / len(pairs)
            rappel = nb_correspondances_note / len(alignements_note)
            f_mesure = 2 * precision * rappel / (precision + rappel)

            print(precision)
            print(rappel)
            print(f_mesure)

        elif (propriete == "opus"):
            for e1, e2 in pairs:
                if (e1, e2) in alignements_opus or (e2, e1) in alignements_opus:
                    nb_correspondances_opus += 1
            # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
            precision = nb_correspondances_opus / len(pairs)
            rappel = nb_correspondances_opus / len(alignements_opus)
            f_mesure = 2 * precision * rappel / (precision + rappel)

            print(precision)
            print(rappel)
            print(f_mesure)

        elif (propriete == "compositeur"):
            for e1, e2 in pairs:
                if (e1, e2) in alignements_compositeur or (e2, e1) in alignements_compositeur:
                    nb_correspondances_compositeur += 1
            # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
            precision = nb_correspondances_compositeur / len(pairs)
            rappel = nb_correspondances_compositeur / len(alignements_compositeur)
            f_mesure = 2 * precision * rappel / (precision + rappel)

            print(precision)
            print(rappel)
            print(f_mesure)
            
        elif (propriete == "titre"):
            for e1, e2 in pairs:
                if (e1, e2) in alignements_titre or (e2, e1) in alignements_titre:
                    nb_correspondances_titre += 1
            # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
            precision = nb_correspondances_titre / len(pairs)
            rappel = nb_correspondances_titre / len(alignements_titre)
            f_mesure = 2 * precision * rappel / (precision + rappel)

            print(precision)
            print(rappel)
            print(f_mesure)
            
        elif (propriete == "genre"):
            for e1, e2 in pairs:
                if (e1, e2) in alignements_genre or (e2, e1) in alignements_genre:
                    nb_correspondances_genre += 1
            # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
            precision = nb_correspondances_genre / len(pairs)
            rappel = nb_correspondances_genre / len(alignements_genre)
            f_mesure = 2 * precision * rappel / (precision + rappel)

            print(precision)
            print(rappel)
            print(f_mesure)
        
        else:
            print("Cette propriete n'existe pas")
            return 0
        
    nb_correspondances = nb_correspondances_clef+ \
                            nb_correspondances_compositeur+ \
                            nb_correspondances_genre+ \
                            nb_correspondances_note+ \
                            nb_correspondances_titre+ \
                            nb_correspondances_opus
        
    # Comparer chaque paire d'URI extraite du fichier texte avec les paires d'URI extraites du fichier RDF d'alignement
    nb_correspondances = 0
    for e1, e2 in pairs:
        if (e1, e2) in alignments or (e2, e1) in alignments:
            nb_correspondances += 1

    print(nb_correspondances)

    # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
    precision = nb_correspondances / len(pairs)
    rappel = nb_correspondances / len(alignments)
    f_mesure = 2 * precision * rappel / (precision + rappel)


    print(precision)
    print(rappel)
    print(f_mesure)




validation("Resultat/resultat_titre_jaro.ttl", ["titre"])

#############################################
# Reste a modifer ça



"""
# Comparer chaque paire d'URI extraite du fichier texte avec les paires d'URI extraites du fichier RDF d'alignement
nb_correspondances = 0
for e1, e2 in pairs:
    if (e1, e2) in alignments or (e2, e1) in alignments:
        nb_correspondances += 1

#print(nb_correspondances)

# Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
precision = nb_correspondances / len(pairs)
rappel = nb_correspondances / len(alignments)
f_mesure = 2 * precision * rappel / (precision + rappel)


print(precision)
print(rappel)
print(f_mesure)
"""