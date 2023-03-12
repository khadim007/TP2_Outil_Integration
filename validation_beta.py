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
    
    #print(pairs)
    
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

            return (precision, rappel, f_mesure)

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

            return (precision, rappel, f_mesure)

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

            return (precision, rappel, f_mesure)

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
            
            return (precision, rappel, f_mesure)

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
            
            return (precision, rappel, f_mesure)

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

            return (precision, rappel, f_mesure)
        
        else:
            print("Cette propriete n'existe pas")
            exit(0)
    """
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

    print("nb_correspondances = ",nb_correspondances)

    # Calculer la précision, le rappel et la f-mesure en fonction du seuil de similarité choisi
    precision = nb_correspondances / len(pairs)
    rappel = nb_correspondances / len(alignments)
    f_mesure = 2 * precision * rappel / (precision + rappel)

    print(precision)
    print(rappel)
    print(f_mesure)

    """


precision_jaro_000, recall_jaro_000, f_precision_jaro_000 = validation("Resultat/resultat_titre_jaro_000.ttl", ["titre"])
precision_jaro_010, recall_jaro_010, f_precision_jaro_010 = validation("Resultat/resultat_titre_jaro_010.ttl", ["titre"])
precision_jaro_020, recall_jaro_020, f_precision_jaro_020 = validation("Resultat/resultat_titre_jaro_020.ttl", ["titre"])
precision_jaro_030, recall_jaro_030, f_precision_jaro_030 = validation("Resultat/resultat_titre_jaro_030.ttl", ["titre"])
precision_jaro_040, recall_jaro_040, f_precision_jaro_040 = validation("Resultat/resultat_titre_jaro_040.ttl", ["titre"])
precision_jaro_050, recall_jaro_050, f_precision_jaro_050 = validation("Resultat/resultat_titre_jaro_050.ttl", ["titre"])
precision_jaro_060, recall_jaro_060, f_precision_jaro_060 = validation("Resultat/resultat_titre_jaro_060.ttl", ["titre"])
precision_jaro_070, recall_jaro_070, f_precision_jaro_070 = validation("Resultat/resultat_titre_jaro_070.ttl", ["titre"])
precision_jaro_080, recall_jaro_080, f_precision_jaro_080 = validation("Resultat/resultat_titre_jaro_080.ttl", ["titre"])
precision_jaro_090, recall_jaro_090, f_precision_jaro_090 = validation("Resultat/resultat_titre_jaro_090.ttl", ["titre"])
precision_jaro_100, recall_jaro_100, f_precision_jaro_100 = validation("Resultat/resultat_titre_jaro_100.ttl", ["titre"])


precision_jaccard_000, recall_jaccard_000, f_precision_jaccard_000 = validation("Resultat/resultat_titre_jaccard_000.ttl", ["titre"])
precision_jaccard_010, recall_jaccard_010, f_precision_jaccard_010 = validation("Resultat/resultat_titre_jaccard_010.ttl", ["titre"])
precision_jaccard_020, recall_jaccard_020, f_precision_jaccard_020 = validation("Resultat/resultat_titre_jaccard_020.ttl", ["titre"])
precision_jaccard_030, recall_jaccard_030, f_precision_jaccard_030 = validation("Resultat/resultat_titre_jaccard_030.ttl", ["titre"])
precision_jaccard_040, recall_jaccard_040, f_precision_jaccard_040 = validation("Resultat/resultat_titre_jaccard_040.ttl", ["titre"])
precision_jaccard_050, recall_jaccard_050, f_precision_jaccard_050 = validation("Resultat/resultat_titre_jaccard_050.ttl", ["titre"])
precision_jaccard_060, recall_jaccard_060, f_precision_jaccard_060 = validation("Resultat/resultat_titre_jaccard_060.ttl", ["titre"])
precision_jaccard_070, recall_jaccard_070, f_precision_jaccard_070 = validation("Resultat/resultat_titre_jaccard_070.ttl", ["titre"])
precision_jaccard_080, recall_jaccard_080, f_precision_jaccard_080 = validation("Resultat/resultat_titre_jaccard_080.ttl", ["titre"])
precision_jaccard_090, recall_jaccard_090, f_precision_jaccard_090 = validation("Resultat/resultat_titre_jaccard_090.ttl", ["titre"])
precision_jaccard_100, recall_jaccard_100, f_precision_jaccard_100 = validation("Resultat/resultat_titre_jaccard_100.ttl", ["titre"])


precision_mongeelkan_000, recall_mongeelkan_000, f_precision_mongeelkan_000 = validation("Resultat/resultat_titre_mongeelkan_000.ttl", ["titre"])
precision_mongeelkan_010, recall_mongeelkan_010, f_precision_mongeelkan_010 = validation("Resultat/resultat_titre_mongeelkan_010.ttl", ["titre"])
precision_mongeelkan_020, recall_mongeelkan_020, f_precision_mongeelkan_020 = validation("Resultat/resultat_titre_mongeelkan_020.ttl", ["titre"])
precision_mongeelkan_030, recall_mongeelkan_030, f_precision_mongeelkan_030 = validation("Resultat/resultat_titre_mongeelkan_030.ttl", ["titre"])
precision_mongeelkan_040, recall_mongeelkan_040, f_precision_mongeelkan_040 = validation("Resultat/resultat_titre_mongeelkan_040.ttl", ["titre"])
precision_mongeelkan_050, recall_mongeelkan_050, f_precision_mongeelkan_050 = validation("Resultat/resultat_titre_mongeelkan_050.ttl", ["titre"])
precision_mongeelkan_060, recall_mongeelkan_060, f_precision_mongeelkan_060 = validation("Resultat/resultat_titre_mongeelkan_060.ttl", ["titre"])
precision_mongeelkan_070, recall_mongeelkan_070, f_precision_mongeelkan_070 = validation("Resultat/resultat_titre_mongeelkan_070.ttl", ["titre"])
precision_mongeelkan_080, recall_mongeelkan_080, f_precision_mongeelkan_080 = validation("Resultat/resultat_titre_mongeelkan_080.ttl", ["titre"])
precision_mongeelkan_090, recall_mongeelkan_090, f_precision_mongeelkan_090 = validation("Resultat/resultat_titre_mongeelkan_090.ttl", ["titre"])
precision_mongeelkan_100, recall_mongeelkan_100, f_precision_mongeelkan_100 = validation("Resultat/resultat_titre_mongeelkan_100.ttl", ["titre"])


precision_numsimilarity_000, recall_numsimilarity_000, f_precision_numsimilarity_000 = validation("Resultat/resultat_titre_numsimilarity_000.ttl", ["titre"])
precision_numsimilarity_010, recall_numsimilarity_010, f_precision_numsimilarity_010 = validation("Resultat/resultat_titre_numsimilarity_010.ttl", ["titre"])
precision_numsimilarity_020, recall_numsimilarity_020, f_precision_numsimilarity_020 = validation("Resultat/resultat_titre_numsimilarity_020.ttl", ["titre"])
precision_numsimilarity_030, recall_numsimilarity_030, f_precision_numsimilarity_030 = validation("Resultat/resultat_titre_numsimilarity_030.ttl", ["titre"])
precision_numsimilarity_040, recall_numsimilarity_040, f_precision_numsimilarity_040 = validation("Resultat/resultat_titre_numsimilarity_040.ttl", ["titre"])
precision_numsimilarity_050, recall_numsimilarity_050, f_precision_numsimilarity_050 = validation("Resultat/resultat_titre_numsimilarity_050.ttl", ["titre"])
precision_numsimilarity_060, recall_numsimilarity_060, f_precision_numsimilarity_060 = validation("Resultat/resultat_titre_numsimilarity_060.ttl", ["titre"])
precision_numsimilarity_070, recall_numsimilarity_070, f_precision_numsimilarity_070 = validation("Resultat/resultat_titre_numsimilarity_070.ttl", ["titre"])
precision_numsimilarity_080, recall_numsimilarity_080, f_precision_numsimilarity_080 = validation("Resultat/resultat_titre_numsimilarity_080.ttl", ["titre"])
precision_numsimilarity_090, recall_numsimilarity_090, f_precision_numsimilarity_090 = validation("Resultat/resultat_titre_numsimilarity_090.ttl", ["titre"])
precision_numsimilarity_100, recall_numsimilarity_100, f_precision_numsimilarity_100 = validation("Resultat/resultat_titre_numsimilarity_100.ttl", ["titre"])

precision_ngram_000, recall_ngram_000, f_precision_ngram_000 = validation("Resultat/resultat_titre_ngram_000.ttl", ["titre"])
precision_ngram_010, recall_ngram_010, f_precision_ngram_010 = validation("Resultat/resultat_titre_ngram_010.ttl", ["titre"])
precision_ngram_020, recall_ngram_020, f_precision_ngram_020 = validation("Resultat/resultat_titre_ngram_020.ttl", ["titre"])
precision_ngram_030, recall_ngram_030, f_precision_ngram_030 = validation("Resultat/resultat_titre_ngram_030.ttl", ["titre"])
precision_ngram_040, recall_ngram_040, f_precision_ngram_040 = validation("Resultat/resultat_titre_ngram_040.ttl", ["titre"])
precision_ngram_050, recall_ngram_050, f_precision_ngram_050 = validation("Resultat/resultat_titre_ngram_050.ttl", ["titre"])
precision_ngram_060, recall_ngram_060, f_precision_ngram_060 = validation("Resultat/resultat_titre_ngram_060.ttl", ["titre"])
precision_ngram_070, recall_ngram_070, f_precision_ngram_070 = validation("Resultat/resultat_titre_ngram_070.ttl", ["titre"])
precision_ngram_080, recall_ngram_080, f_precision_ngram_080 = validation("Resultat/resultat_titre_ngram_080.ttl", ["titre"])
precision_ngram_090, recall_ngram_090, f_precision_ngram_090 = validation("Resultat/resultat_titre_ngram_090.ttl", ["titre"])
precision_ngram_100, recall_ngram_100, f_precision_ngram_100 = validation("Resultat/resultat_titre_ngram_100.ttl", ["titre"])

precision_levenshtein_000, recall_levenshtein_000, f_precision_levenshtein_000 = validation("Resultat/resultat_titre_levenshtein_000.ttl", ["titre"])
precision_levenshtein_010, recall_levenshtein_010, f_precision_levenshtein_010 = validation("Resultat/resultat_titre_levenshtein_010.ttl", ["titre"])
precision_levenshtein_020, recall_levenshtein_020, f_precision_levenshtein_020 = validation("Resultat/resultat_titre_levenshtein_020.ttl", ["titre"])
precision_levenshtein_030, recall_levenshtein_030, f_precision_levenshtein_030 = validation("Resultat/resultat_titre_levenshtein_030.ttl", ["titre"])
precision_levenshtein_040, recall_levenshtein_040, f_precision_levenshtein_040 = validation("Resultat/resultat_titre_levenshtein_040.ttl", ["titre"])
precision_levenshtein_050, recall_levenshtein_050, f_precision_levenshtein_050 = validation("Resultat/resultat_titre_levenshtein_050.ttl", ["titre"])
precision_levenshtein_060, recall_levenshtein_060, f_precision_levenshtein_060 = validation("Resultat/resultat_titre_levenshtein_060.ttl", ["titre"])
precision_levenshtein_070, recall_levenshtein_070, f_precision_levenshtein_070 = validation("Resultat/resultat_titre_levenshtein_070.ttl", ["titre"])
precision_levenshtein_080, recall_levenshtein_080, f_precision_levenshtein_080 = validation("Resultat/resultat_titre_levenshtein_080.ttl", ["titre"])
precision_levenshtein_090, recall_levenshtein_090, f_precision_levenshtein_090 = validation("Resultat/resultat_titre_levenshtein_090.ttl", ["titre"])
precision_levenshtein_100, recall_levenshtein_100, f_precision_levenshtein_100 = validation("Resultat/resultat_titre_levenshtein_100.ttl", ["titre"])

precision_jarowrinkler_000, recall_jarowrinkler_000, f_precision_jarowrinkler_000 = validation("Resultat/resultat_titre_jarowrinkler_000.ttl", ["titre"])
precision_jarowrinkler_010, recall_jarowrinkler_010, f_precision_jarowrinkler_010 = validation("Resultat/resultat_titre_jarowrinkler_010.ttl", ["titre"])
precision_jarowrinkler_020, recall_jarowrinkler_020, f_precision_jarowrinkler_020 = validation("Resultat/resultat_titre_jarowrinkler_020.ttl", ["titre"])
precision_jarowrinkler_030, recall_jarowrinkler_030, f_precision_jarowrinkler_030 = validation("Resultat/resultat_titre_jarowrinkler_030.ttl", ["titre"])
precision_jarowrinkler_040, recall_jarowrinkler_040, f_precision_jarowrinkler_040 = validation("Resultat/resultat_titre_jarowrinkler_040.ttl", ["titre"])
precision_jarowrinkler_050, recall_jarowrinkler_050, f_precision_jarowrinkler_050 = validation("Resultat/resultat_titre_jarowrinkler_050.ttl", ["titre"])
precision_jarowrinkler_060, recall_jarowrinkler_060, f_precision_jarowrinkler_060 = validation("Resultat/resultat_titre_jarowrinkler_060.ttl", ["titre"])
precision_jarowrinkler_070, recall_jarowrinkler_070, f_precision_jarowrinkler_070 = validation("Resultat/resultat_titre_jarowrinkler_070.ttl", ["titre"])
precision_jarowrinkler_080, recall_jarowrinkler_080, f_precision_jarowrinkler_080 = validation("Resultat/resultat_titre_jarowrinkler_080.ttl", ["titre"])
precision_jarowrinkler_090, recall_jarowrinkler_090, f_precision_jarowrinkler_090 = validation("Resultat/resultat_titre_jarowrinkler_090.ttl", ["titre"])
precision_jarowrinkler_100, recall_jarowrinkler_100, f_precision_jarowrinkler_100 = validation("Resultat/resultat_titre_jarowrinkler_100.ttl", ["titre"])

precision_uriequality_000, recall_uriequality_000, f_precision_uriequality_000 = validation("Resultat/resultat_titre_uriequality_000.ttl", ["titre"])
precision_uriequality_010, recall_uriequality_010, f_precision_uriequality_010 = validation("Resultat/resultat_titre_uriequality_010.ttl", ["titre"])
precision_uriequality_020, recall_uriequality_020, f_precision_uriequality_020 = validation("Resultat/resultat_titre_uriequality_020.ttl", ["titre"])
precision_uriequality_030, recall_uriequality_030, f_precision_uriequality_030 = validation("Resultat/resultat_titre_uriequality_030.ttl", ["titre"])
precision_uriequality_040, recall_uriequality_040, f_precision_uriequality_040 = validation("Resultat/resultat_titre_uriequality_040.ttl", ["titre"])
precision_uriequality_050, recall_uriequality_050, f_precision_uriequality_050 = validation("Resultat/resultat_titre_uriequality_050.ttl", ["titre"])
precision_uriequality_060, recall_uriequality_060, f_precision_uriequality_060 = validation("Resultat/resultat_titre_uriequality_060.ttl", ["titre"])
precision_uriequality_070, recall_uriequality_070, f_precision_uriequality_070 = validation("Resultat/resultat_titre_uriequality_070.ttl", ["titre"])
precision_uriequality_080, recall_uriequality_080, f_precision_uriequality_080 = validation("Resultat/resultat_titre_uriequality_080.ttl", ["titre"])
precision_uriequality_090, recall_uriequality_090, f_precision_uriequality_090 = validation("Resultat/resultat_titre_uriequality_090.ttl", ["titre"])
precision_uriequality_100, recall_uriequality_100, f_precision_uriequality_100 = validation("Resultat/resultat_titre_uriequality_100.ttl", ["titre"])


import matplotlib.pyplot as plt 

x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
f_precision_jaro = [f_precision_jaro_000, f_precision_jaro_010,
                    f_precision_jaro_020, f_precision_jaro_030,
                    f_precision_jaro_040, f_precision_jaro_050,
                    f_precision_jaro_060, f_precision_jaro_070,
                    f_precision_jaro_080, f_precision_jaro_090,
                    f_precision_jaro_100]

f_precision_jaccard = [f_precision_jaccard_000, f_precision_jaccard_010,
                       f_precision_jaccard_020, f_precision_jaccard_030,
                       f_precision_jaccard_040, f_precision_jaccard_050,
                       f_precision_jaccard_060, f_precision_jaccard_070,
                       f_precision_jaccard_080, f_precision_jaccard_090,
                       f_precision_jaccard_100]

f_precision_mongeelkan = [f_precision_mongeelkan_000, f_precision_mongeelkan_010,
                          f_precision_mongeelkan_020, f_precision_mongeelkan_030,
                          f_precision_mongeelkan_040, f_precision_mongeelkan_050,
                          f_precision_mongeelkan_060, f_precision_mongeelkan_070,
                          f_precision_mongeelkan_080, f_precision_mongeelkan_090,
                          f_precision_mongeelkan_100]

f_precision_numsimilarity = [f_precision_numsimilarity_000, f_precision_numsimilarity_010,
                             f_precision_numsimilarity_020, f_precision_numsimilarity_030,
                             f_precision_numsimilarity_040, f_precision_numsimilarity_050,
                             f_precision_numsimilarity_060, f_precision_numsimilarity_070,
                             f_precision_numsimilarity_080, f_precision_numsimilarity_090,
                             f_precision_numsimilarity_100]

f_precision_ngram = [f_precision_ngram_000, f_precision_ngram_010,
                     f_precision_ngram_020, f_precision_ngram_030,
                     f_precision_ngram_040, f_precision_ngram_050,
                     f_precision_ngram_060, f_precision_ngram_070,
                     f_precision_ngram_080, f_precision_ngram_090,
                     f_precision_ngram_100]

f_precision_levenshtein = [f_precision_levenshtein_000, f_precision_levenshtein_010,
                           f_precision_levenshtein_020, f_precision_levenshtein_030,
                           f_precision_levenshtein_040, f_precision_levenshtein_050, 
                           f_precision_levenshtein_060, f_precision_levenshtein_070,
                           f_precision_levenshtein_080, f_precision_levenshtein_090,
                           f_precision_levenshtein_100]

f_precision_jarowrinkler = [f_precision_jarowrinkler_000, f_precision_jarowrinkler_010,
                            f_precision_jarowrinkler_020, f_precision_jarowrinkler_030,
                            f_precision_jarowrinkler_040, f_precision_jarowrinkler_050,
                            f_precision_jarowrinkler_060, f_precision_jarowrinkler_070, 
                            f_precision_jarowrinkler_080, f_precision_jarowrinkler_090,
                            f_precision_jarowrinkler_100]


f_precision_uriequality = [f_precision_uriequality_000, f_precision_uriequality_010,
                           f_precision_uriequality_020, f_precision_uriequality_030,
                           f_precision_uriequality_040, f_precision_uriequality_050,
                           f_precision_uriequality_060, f_precision_uriequality_070,
                           f_precision_uriequality_080, f_precision_uriequality_090,
                           f_precision_uriequality_100]

marker_size = 5

plt.plot(x, f_precision_jaro, color="blue", label="Jaro", marker='o', markersize=marker_size)
plt.plot(x, f_precision_jaccard, color="red", label="Jaccard", marker='s', markersize=marker_size)
plt.plot(x, f_precision_mongeelkan, color="green", label="MongeElkan", marker='^', markersize=marker_size)
plt.plot(x, f_precision_numsimilarity, color="black", label="NumSimilarity", marker='x', markersize=10)
plt.plot(x, f_precision_ngram, color="yellow", label="Ngram", marker='*', markersize=marker_size)
plt.plot(x, f_precision_levenshtein, color="maroon", label="Levenshtein", marker='D', markersize=marker_size)
plt.plot(x, f_precision_jarowrinkler, color="orange", label="JaroWrinkler", marker='P', markersize=marker_size)
plt.plot(x, f_precision_uriequality, color="purple", label="UriEquality", marker='H', markersize=marker_size)

# ajouter une légende en dehors du graphe
plt.legend(bbox_to_anchor=(1.05, 0.7), loc='upper left')

plt.xlabel("Seuil")
plt.ylabel("F-mesure")

# affiche le graphe
plt.show()

#ajouter un graphe avec les precision, recall et f-mesure sur une seule propriete

#ajouter un graphe avec chaque propriete le nombre des tuples dans 
#le fichier de reference et dans le nombre tuples dans le fichier resultat
