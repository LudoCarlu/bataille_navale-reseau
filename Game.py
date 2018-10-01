#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 23:29:41 2018

@author: ludoviccarlu
"""
global login_admin, mdp
login_admin = 'Admin'
mdp = 'Admin'


class Plateau:

    def __init__(self, size):
        self.plateau = []
        self.size = size
        self.list_bateau = []  ## Pour vérifier si le bateau a été touché

        for i in range(size):
            self.plateau.append(['~'] * size)

    def display(self):

        for i in range(0, self.size):
            for j in range(0, self.size):
                print(self.plateau[i][j], end=' ')
            print()

    def afficher_plateau(self):
        plateau = ""
        for i in range(0, self.size):
            for j in range(0, self.size):
                plateau = plateau + self.plateau[i][j] + ' '
            plateau = plateau + '\n'

        return plateau

    def afficher_plateau_client(self):
        plateau = ""
        for i in range(0, self.size):
            if len(str(i)) == 1:
                plateau += str(i) + "  "
            else:
                plateau += str(i) + " "

            for j in range(0, self.size):
                if self.plateau[i][j] in ('T', 'C', '~'):
                    plateau = plateau + self.plateau[i][j] + ' '
                else:
                    plateau = plateau + '~' + ' '

            plateau = plateau + '\n'

        for j in range(0, self.size):
            plateau += str(j) + ' '

        plateau += '\n'

        return plateau

    def get_plateau(self):
        return self.plateau

    def display_bateau_touche(self):

        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.plateau[i][j] in ('T', 'C'):
                    print(self.plateau[i][j], end=' ')
                else:
                    print('~', end=' ')
            print()

    # def detecter_bateau_touche(self, coord):
    #     coordx = coord[0]  # #1
    #     coordy = coord[1]  # #4  -> La tete est a 1, 1
    #
    #     for bateau in self.list_bateau:
    #         head_coordx = bateau.head_coord[0]
    #         head_coordy = bateau.head_coord[1]
    #         if bateau.orientation == 'horizontale' and coordx in \
    #                 range(head_coordx, (head_coordx + bateau.size + 1)):
    #             bateau.nb_touche = bateau.nb_touche + 1
    #             return bateau
    #         elif bateau.orientation == 'verticale' and coordy in \
    #                 range(head_coordy, (head_coordy + bateau.size + 1)):
    #             bateau.nb_touche = bateau.nb_touche + 1
    #             return bateau
    #
    # def detecter_bateau_coule(self, bateau):
    #     if bateau.size == bateau.nb_touche:
    #         print(bateau.nb_touche)
    #         print("Coulée!")
    #         bateau.etat = 1
    #         for i in range(bateau.size):
    #             if bateau.orientation == 'horizontale':
    #                 self.plateau[bateau.head_coord[0]][bateau.head_coord[1] + i] = 'C'
    #             else:
    #                 self.plateau[bateau.head_coord[1] + i][bateau.head_coord[0]] = 'C'
    #         return 'C'

    def detecter_bateau_touche_2(self, coord):
        coordx = coord[0]
        coordy = coord[1]

        for b in self.list_bateau:

            tete_x = b.head_coord[0]
            tete_y = b.head_coord[1]

            if b.orientation == "horizontale":
                if tete_x == coordx:  # La tete sur la meme ligne que Y
                    if coordy in range(tete_y, tete_y + b.size+1):
                        b.nb_touche += 1
                        return b

            if b.orientation == "verticale":
                if tete_y == coordy:
                    if coordx in range(tete_x, tete_x + b.size):
                        b.nb_touche += 1
                        return b

    def detecter_bateau_coule_2(self, bateau):

        tete_x = bateau.head_coord[0]
        tete_y = bateau.head_coord[1]

        if bateau.size == bateau.nb_touche:
            bateau.etat = 1

            for i in range(bateau.size):
                if bateau.orientation == "horizontale":
                    self.plateau[tete_x][tete_y+ i] = 'C'
                elif bateau.orientation == "verticale":
                    self.plateau[tete_x+i][tete_y] = 'C'

            return 'C'

    def is_partie_finie(self):
        cpt = 0
        for b in self.list_bateau:
            if b.etat == 1:
                cpt += 1

        if cpt == len(self.list_bateau):
            return True
        else:
            return False


class Bateau:
    '''
    type de bateau = 'grand','petit'
    etat : 0 en vie
    etat : 1 coulé
    size : taille du bateau
    nb_touche : nombre de case touché (si nb_touche==size) alors etat=3
    head_cord = tableau (x,y)
    orientation = 'horizontal','vertical'
    tableau_etat = tableau[size]
    '''

    def __init__(self, type_bateau, orientation, head_coord):
        if type_bateau == 'grand':
            self.size = 6
        elif type_bateau == 'moyen':
            self.size = 4
        elif type_bateau == 'petit':
            self.size = 2
        self.etat = 0
        self.nb_touche = 0
        self.orientation = orientation
        self.head_coord = head_coord
        self.tableau_etat = [0] * self.size

    def __str__(self):
        bateau = ''
        for i in range(self.size):
            if self.tableau_etat[i] == 0:
                bateau += '-'
            else:
                bateau += 'X'
        return bateau


class Joueur:
    name = ""
    connexion = None
    score = 0
    tour = False

    def __init__(self, name):

        self.name = name
        self.score = 0

    def __init__(self, name, connexion):

        self.name = name
        self.score = 0
        self.connexion = connexion

    def get_connexion(self):
        return self.connexion

    def get_name(self):
        return self.name

    def set_connexion(self, c):
        self.connexion = c

    def get_tour(self):
        return self.tour

    def set_tour(self, tour):
        self.tour = tour

    def add_point(self, nbpoint):
        self.score += nbpoint

    def get_score(self):
        return self.score

    def lancer_tir(self, classplateau, coord):
        plateau = classplateau.plateau
        coordx = coord[0]
        coordy = coord[1]
        if plateau[coordx][coordy] == '~':
            return 'Raté !'
        elif plateau[coordx][coordy] == 'B':
            plateau[coordx][coordy] = 'T'
            bateau = classplateau.detecter_bateau_touche_2((coordx, coordy))
            is_coule = classplateau.detecter_bateau_coule_2(bateau)

            if is_coule == "C":
                return 'Coulé !'
            else:
                return 'Touché !'
        elif plateau[coordx][coordy] == 'T' or plateau[coordx][coordy] == 'C':
            return 'Déja touché..'


class Administrateur:
    name = ""
    connexion = None

    def __init__(self, name):

        self.name = name

    def __init__(self, name, connexion):

        self.name = name
        self.connexion = connexion

    def get_connexion(self):
        return self.connexion

    def get_name(self):
        return self.name

    def set_connexion(self, c):
        self.connexion = c

    def placer_bateau(self, classplateau, boat):
        plateau = classplateau.plateau
        coordx = boat.head_coord[0]

        coordy = boat.head_coord[1]
        taille = boat.size
        orientation = boat.orientation
        try:
            for i in range(taille):  ## Verif du placement
                if orientation == 'horizontale' and plateau[coordx][coordy + i] in ('B', '2'):
                    raise Exception(" Placement impossible ")
                elif orientation == 'verticale' and plateau[coordx + i][coordy] in ('B', '2'):
                    raise Exception(" Placement impossible ")
            ## Placement
            for i in range(taille):
                if orientation == 'horizontale':
                    plateau[coordx][coordy + i] = 'B'
                elif orientation == 'verticale':
                    plateau[coordx + i][coordy] = 'B'
            classplateau.list_bateau.append(boat)
            return True
        except Exception as e:
            print(str(e) + ' Placement impossible')
            return False

#
# pla = Plateau(10)
# adm = Administrateur("ok", "ok")
# adm.placer_bateau(pla, Bateau('grand', 'horizontale', (1, 1)))
# pla.display()
# joueur = Joueur('max', "ok")
# joueur.lancer_tir(pla, (1, 1))
# pla.display()
#
#
# joueur.lancer_tir(pla, (1, 2))
#
# def main():
#     board = Plateau(8)
#     print(board.display())
#     print(board.display_bateau_touche())
# #