import py_stringmatching as psm
import SPARQLWrapper
import warnings

from mesures import *
from rdflib import *
from rdflib import *
from SPARQLWrapper import SPARQLWrapper, JSON


def openFile(fileName):
    with open(fileName, "w") as f:
        f.close()

def compareExpressions(graphe1, graphe2, initP, initM, seuil):
    expressions1 = getExpressions(graphe1)
    expressions2 = getExpressions(graphe2)

    for exp1 in expressions1:
        for exp2 in expressions2:
            somme = 0
            nombre = 0
            for cle, valeur in initP.items():
                if valeur > 0:
                    somme += compareProprietes(exp1, exp2, graphe1, graphe2, cle, initM)
                    nombre += 1

            if nombre == 0: sortie(10, initM)
            if(somme / nombre) >= seuil:
                print(exp1.expression, " <----> ", exp1.expression)
                updateFichier("resultat.ttl", exp1.expression, exp2.expression)
    print("La comparaison est terminee")

def getExpressions(graphe):
    req = """
        PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
        SELECT DISTINCT ?expression
        WHERE{
            ?expression a efrbroo:F22_Self-Contained_Expression.
        }"""
    res = graphe.query(req)
    return res

def compareProprietes(exp1, exp2, graphe1, graphe2, propriete, initM):
    nombre = 0
    somme = 0
    proprietes1 = []
    proprietes2 = []
    for row in exp1:
        proprietes1.append(getPropriete(propriete, row, graphe1))
    for row in exp2:
        proprietes2.append(getPropriete(propriete, row, graphe2))

    for cle, valeur in initM.items():
        if(cle == "ngram1"):
            if valeur > 0:
                somme += compareNgram(proprietes1, proprietes2, initM['ngram2'], ngram1) * initM[cle]
                nombre += initM[cle]
        elif(cle == "ngram2"): continue
        else:
            if valeur > 0:
                somme += compare(proprietes1, proprietes2, cle) * initM[cle]
                nombre += initM[cle]

    if nombre == 0: sortie(11, initM)
    return somme / nombre

def getPropriete(propriete, expression, graphe):
    if (propriete == "clef"):
        req = """ 
            PREFIX mus: <http://data.doremus.org/ontology#>
            SELECT ?expression ?clef
            WHERE{
                ?expression mus:U11_has_key ?clef.
                FILTER(isIRI(?clef)).
            }"""
    elif (propriete == "note"):
        req = """ 
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            SELECT ?expression ?note
            WHERE{
                ?expression ecrm:P3_has_note ?note.
            }"""
    elif (propriete == "opus"):
        req = """ 
            PREFIX mus: <http://data.doremus.org/ontology#>
            SELECT ?expression ?opus
            WHERE{
                ?expression mus:U17_has_opus_statement / mus:U42_has_opus_number ?opus.
            }"""
    elif (propriete == "compositeur"):
        req = """
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            SELECT ?expression ?compositeur
            WHERE{
                ?expression a efrbroo:F22_Self-Contained_Expression .
                ?expCreation efrbroo:R17_created ?expression ;
                ecrm:P9_consists_of / ecrm:P14_carried_out_by ?compositeur ;
            }"""
    elif (propriete == "titre"):
        req = """
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            SELECT ?expression ?title
            WHERE {
                ?expression ecrm:P102_has_title ?title .
            }"""
    elif (propriete == "genre"):
        req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            SELECT ?expression ?genre
            WHERE {
                ?expression mus:U12_has_genre ?genre.
                FILTER (isIRI(?genre))
            }"""
    else:
        return 0

    tab = graphe.query(req, initBindings={'expression': expression})
    resultat = []
    for i in tab:
        resultat.append(str(i[1]))

    return resultat

def compare(p1, p2, fonc):
    somme = []
    for e1 in p1:
        for e2 in p2:
            somme.append(appel(fonc, e1, e2))
    print(".")
    return max(somme)

def compareNgram(p1, p2, n2, fonc):
    somme = []
    for e1 in p1:
        for e2 in p2:
            somme.append(fonc(str(e1), str(e2), n2))        
    print(".")
    return max(somme)

def updateFichier(fileName, exp1, exp2):
    content = "<" + str(exp1) + ">\n    <http://www.w3.org/2002/07/owl#sameAs>\n<" + str(exp2) + ">\n\n"
    with open(fileName, "a") as f:
        f.write(content)
        f.close()

def sortie(s, initM):
    if(s == 0):
        print("\n\nVous n'avez pas choisi de seuil !!")
    elif(s == 10):
        print("\n\nVous n'avez pas choisi de proprietes !!")
    elif(s == 11):
        print("\n\nVous n'avez pas choisi de mesures !!")
    else:
        i = 0
        for cle, valeur in initM.items():
            if(i == (s-1)):
                print("\n\nVous n'avez pas choisi de poid pour la mesure "+cle+" !!")
            i+=1
    exit(0)