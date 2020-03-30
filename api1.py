"""Fonctions utiles au bon fonctionnement lors de l'intéraction avec le serveur"""
import requests


URL = 'https://python.gel.ulaval.ca/quoridor/api/'

def lister_parties(idul):
    """Retourne une liste de partie avec leur id et leur état"""
    rep = requests.get(URL+'lister/', params={'idul' : idul})
    if rep.status_code != 200:
        raise RuntimeError(rep['message'])
    rep = rep.json()
    return rep

def débuter_partie(idul):
    """Débute une partie de Quoridor selon l'identité du joueur"""
    rep = requests.post(URL+'débuter/', data={'idul' : idul})
    rep = rep.json()
    if 'message' in rep.keys():
        raise RuntimeError(rep['message'])
    return (rep['id'], rep['état'])

def jouer_coup(id_partie, type_coup, position):
    """Met la planche de jeu à jour après chaque coup"""
    r = requests.post(URL+'jouer/', data={'id' : id_partie, 'type' : type_coup, 'pos' : position})
    rep = r.json()
    if 'message' in rep.keys():
        raise RuntimeError(rep['message'])
    elif 'gagnant' in rep.keys():
        raise StopIteration(rep['gagnant'])
    else:
        return rep['état']