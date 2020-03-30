"""Modules de base permettant de jouer au jeu"""
import argparse
import api1


def analyser_commande():
    """Encapsule l'idul du joueur"""
    parser = argparse.ArgumentParser(description='Quoridor - phase 1')
    parser.add_argument('idul', help='IDUL du joueur.')
    parser.add_argument('-l', '--lister', dest='lister', action='store_true',
                        help='Lister les identifiants de vos 20 dernières parties.')
    return parser.parse_args()

def afficher_damier_ascii(d):
    """Affiche le damier en fonction des mises à jour effectuées au fil des tours"""
    a = [i for i in range(1, 10)]
    a.reverse()
    board = [['   ' + '-'*35]]
    for b in a:
        board += ([[f'{b} |'] + [' . '] + ([' ']+[' . '])*8 + ['|']] +
                  [['  |'] + ['   '] + ([' ']+['   '])*8 + ['|']])
    board = board[:len(board)-1] + [['--|' + '-'*35], ['  | 1'] + [f'   {i}' for i in range(2, 10)]]
    board[19 - 2*d["joueurs"][0]["pos"][1]][2*d["joueurs"][0]["pos"][0] - 1] = ' 1 '
    board[19 - 2*d["joueurs"][1]["pos"][1]][2*d["joueurs"][1]["pos"][0] - 1] = ' 2 '
    for mur_horizon in d["murs"]["horizontaux"]:
        board[20 - 2*mur_horizon[1]][2*mur_horizon[0] - 1] = '---'
        board[20 - 2*mur_horizon[1]][2*mur_horizon[0]] = '-'
        board[20 - 2*mur_horizon[1]][2*mur_horizon[0] + 1] = '---'
    for mur_verti in d["murs"]["verticaux"]:
        board[19 - 2*mur_verti[1]][2*mur_verti[0] - 2] = '|'
        board[18 - 2*mur_verti[1]][2*mur_verti[0] - 2] = '|'
        board[17 - 2*mur_verti[1]][2*mur_verti[0] - 2] = '|'
    print('Légende: 1 = '+analyser_commande().idul+', 2 = IA')
    for i in enumerate(board):
        print(''.join(board[i[0]]))

if analyser_commande().lister:
    print(api1.lister_parties(analyser_commande().idul))
else:
    DEB = api1.débuter_partie(analyser_commande().idul)
    afficher_damier_ascii(DEB[1])
    EN_JEU = True
    while EN_JEU:
        T = input('Déterminez le type de coup à effectuer (D, MH, MV): ')
        P = input('Quelle Position (x, y) ? : ')
        if T == 'break':
            break
        try:
            afficher_damier_ascii(api1.jouer_coup(DEB[0], T, P))
        except RuntimeError as re:
            print('RuntimeError : ', re)
            NT = input('Déterminez le type de coup à effectuer (D, MH, MV): ')
            NP = input('Quelle Position (x, y) ? : ')
            afficher_damier_ascii(api1.jouer_coup(DEB[0], NT, NP))
        except StopIteration as si:
            print('Vainqueur: ', si)
            break