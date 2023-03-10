import py_stringmatching as psm

def jaro(e1, e2):
    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    else:
        e1 = pretraitementURL(e1)
        e2 = pretraitementURL(e2)
        return psm.Jaro().get_sim_score(str(e1), str(e2))

def jaccar(e1, e2):
    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    else:
        e1 = tokenisation(e1)
        e2 = tokenisation(e2)
        return psm.Jaccard().get_sim_score(e1, e2)

def monge_elkan(e1, e2):
    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    else:
        e1 = tokenisation(e1)
        e2 = tokenisation(e2)
        return psm.MongeElkan().get_raw_score(e1, e2)

def numSimilarity(e1, e2):
    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    elif (e1 == e2):
        return 1.0
    else:
        return 0.0

def ngram1(e1, e2, s):
    e1 = pretraitementURL(e1)
    e2 = pretraitementURL(e2)
    i = 0
    nbr = 0
    while ((i + s) <= len(e1)) or ((i + s) <= len(e2)):
        if e1[i:i + s] == e2[i:i + s]:
            nbr += 1
        i += 1
    if ((min(len(e1), len(e2)) - s) < 0):
        return 0
    return (nbr) / (min(len(e2), len(e1)) - s + 1)

def levenshtein(e1, e2):
    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    else:
        e1 = pretraitementURL(e1)
        e2 = pretraitementURL(e2)
        return psm.Levenshtein().get_sim_score(e1, e2)

def jaroWrinkler(e1, e2):

    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    else:
        e1 = pretraitementURL(e1)
        e2 = pretraitementURL(e2)
        return psm.JaroWinkler().get_sim_score(e1, e2)

def uriEquality(e1, e2):
    if (len(e1) == 0 or len(e2) == 0):
        return 0.0
    elif (pretraitementURL(e1) == pretraitementURL(e2)):
        return 1.0
    else:
        return 0.0

def appel(nom, e1, e2):
    if nom == "jaro":
        return jaro(e1, e2)
    elif nom == "jaccar":
        return jaccar(e1, e2)
    elif nom == "monge_elkan":
        return monge_elkan(e1, e2)
    elif nom == "numSimilarity":
        return numSimilarity(e1, e2)
    elif nom == "levenshtein":
        return levenshtein(e1, e2)
    elif nom == "jaroWrinkler":
        return jaroWrinkler(e1, e2)
    elif nom == "uriEquality":
        return uriEquality(e1, e2)

def pretraitementURL(url):
    token = tokenisation(url)
    resultat = "".join(token)
    return resultat

def tokenisation(str):
    if (type(str) == list):
        token = []
        for elem in str:
            token = list(set(token) | set(elem.split(" ")))
        return token
    elif (isURL(str)):
        token = str.split("/")[-2:]
        return token
    else:
        return str.split(" ")

def isURL(str):
    return str.startswith("http")