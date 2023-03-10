import PySimpleGUI as sg
import warnings

from fonctions import *
from rdflib import *

warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    source = "source.ttl"
    target = "target.ttl"
    resultat = "resultat.ttl"

    seuil = 0.5
    largeur = 700
    longeur = 520
    initP = {"clef": 0, "titre": 0, "note": 0, "genre": 0, "compositeur": 0, "opus": 0}
    initM = {"jaro": 0, "jaccar": 0, "monge_elkan": 0, "numSimilarity": 0, "ngram1": 0, "ngram2": 0, "levenshtein": 0, "jaroWrinkler": 0, "uriEquality": 0}


    graphe1 = Graph()
    graphe2 = Graph()
    graphe1.parse(source)
    graphe2.parse(target)

    openFile(resultat)
    sg.theme('DarkAmber')

    gauche = [
        [sg.T('Choisissez les propriétés: ', font=('Helvetica', 18))],
        [sg.Checkbox('Clef', default=False, key="p1")],
        [sg.Checkbox('Titre', default=False, key="p2")],
        [sg.Checkbox('Note', default=False, key="p3")],
        [sg.Checkbox('Genre', default=False, key="p4")],
        [sg.Checkbox('Compositeur', default=False, key="p5")],
        [sg.Checkbox('Opus', default=False, key="p6")]]
    droite = [
        [sg.T('Choisissez les mesures: ', font=('Helvetica', 18))],
        [sg.Checkbox('Jaro', default=False, key="m1"), sg.T("             "), sg.InputText(size=(10, 2), key='1')],
        [sg.Checkbox('Jaccard', default=False, key="m2"), sg.T("        "), sg.InputText(size=(10, 2), key='2')],
        [sg.Checkbox('Monge Elkan', default=False, key="m3"), sg.T(" "), sg.InputText(size=(10, 2), key='3')],
        [sg.Checkbox('NumSimilarity', default=False, key="m4"), sg.T(""), sg.InputText(size=(10, 2), key='4')],
        [sg.Checkbox('Ngram', default=False, key="m5"), sg.T("           "),sg.InputText(size=(10, 2), key='5')],
        [sg.T("     Ngram Size       "), sg.InputText(size=(10, 2), key='5-2')],
        [sg.Checkbox('Levenshtein', default=False, key="m7"), sg.T("    "), sg.InputText(size=(10, 2), key='7')],
        [sg.Checkbox('JaroWrinkler', default=False, key="m8"), sg.T("   "), sg.InputText(size=(10, 2), key='8')],
        [sg.Checkbox('uriEquality', default=False, key="m9"), sg.T("      "), sg.InputText(size=(10, 2), key='9')]]
    affichage = [
        [sg.T("OUTIL D'INTEGRATION DE DONNEES", justification='center', size=(largeur,1), font=('Helvetica', 22))],
        [sg.HorizontalSeparator(pad=(100, 20))],
        [sg.T("Seuil", font=('Helvetica', 14)), sg.InputText(size=(10, 2), key='0')],
        [sg.HorizontalSeparator(pad=(100, 20))],
        [sg.Col(gauche), sg.VerticalSeparator(), sg.Col(droite)],
        [sg.HorizontalSeparator(pad=(100, 20))],
        [sg.Button('Submit', size=(15, 2))]]
    window = sg.Window('Outil D\'integration', affichage, size=(largeur, longeur), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == 'Submit': 
            seuil = float(values['0'])
            print("seuil : ", seuil)
            i = 1     
            for cle, valeur in initP.items():
                p = "p"+str(i)
                initP[cle] =  1 if values[p] == True else 0
                i+=1
                print(cle," : ", initP[cle])
            i = 1 
            for cle, valeur in initM.items():
                if i == 6:
                    m = "m"+str(i-1)
                    initM[cle] = int(values['5-2']) if values[m] == True else 0 
                else:
                    m = "m"+str(i)
                    initM[cle] =  float(values[str(i)]) if values[m] == True else 0
                i+=1
                print(cle," : ", initM[cle])

            compareExpressions(graphe1, graphe2, initP, initM, seuil)
    window.close()

if __name__ == '__main__':
    main()
