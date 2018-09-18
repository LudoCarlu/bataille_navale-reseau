#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 23:29:41 2018

@author: ludoviccarlu
"""
global login_admin,mdp
login_admin = 'Admin'
mdp = 'Admin'

class Plateau:
    
    def __init__(self, size):
        self.plateau = []
        self.size = size
        self.list_bateau= [] ## Pour vérifier si le bateau a été touché
        
        for i in range (size):
            self.plateau.append(['~'] *size)
        
        
    def display(self):
    
        for i in range (0,self.size):
            for j in range (0, self.size):
                print(self.plateau[i][j], end=' ')
            print()
    
    def display_bateau_touche(self):
        
        for i in range (0,self.size):
            for j in range (0, self.size):
                if self.plateau[i][j] in (-1,2):
                    print(self.plateau[i][j], end=' ')
                else:
                    print('~', end = ' ')
            print()
    def detecter_bateau_touche(self,coord):
        coordy = coord[0] # #1
        coordx = coord[1] # #4  -> La tete est a 1, 1
        for bateau in self.list_bateau:
            head_coordy= bateau.head_coord[0]
            head_coordx= bateau.head_coord[1]
            if bateau.orientation == 'horizontal' and coordx in \
            range(head_coordx,(head_coordx+bateau.size+1)):
                bateau.nb_touche = bateau.nb_touche + 1
                return bateau;
            elif bateau.orientation == 'vertical' and coordy in \
            range(head_coordy,(head_coordy+bateau.size+1)):
                bateau.nb_touche = bateau.nb_touche + 1
                return bateau;
            
    def detecter_bateaux_coule(self,bateau):
            if bateau.size==bateau.nb_touche:
                print("Coulée!")
                bateau.etat = 1
                for i in range(bateau.size):
                    if bateau.orientation == 'horizontal':
                        self.plateau[bateau.head_coord[0]][bateau.head_coord[1]+i] = 'X'
                    else:
                        self.plateau[bateau.head_coord[0]+i][bateau.head_coord[1]] = 'X'
                      
                    
                     
            


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
    
    def __init__(self,type_bateau ,orientation, head_coord):
        if type_bateau=='grand':
            self.size=8
        else:
            self.size=4
        self.etat = 0
        self.nb_touche = 0
        self.orientation = orientation
        self.head_coord = head_coord
        self.tableau_etat = [0] * self.size
        

    def __str__(self):
        bateau=''
        for i in range(self.size):
            if self.tableau_etat[i]==0:
                bateau+='-'
            else:
                bateau+='X'
        return bateau


class Joueur:
    
    def __init__(self, name):
        
        self.name = name
        self.score = 0
    def lancer_tir(self,classplateau,coord):
        plateau = classplateau.plateau
        coordy = coord[0]
        coordx = coord[1]
        if plateau[coordy][coordx] =='~':
            print('Raté!')
        elif plateau[coordy][coordx] =='1':
            print('Touché!')
            plateau[coordy][coordx] ='O'
            bateau = classplateau.detecter_bateau_touche((coordx,coordy))
            classplateau.detecter_bateaux_coule(bateau)
        elif plateau[coordy][coordx] =='O':
            print('Déja touché..')
        
        
      

class Adminstrateur:
    
    def __init__(self, name):
        
        self.name = name

    def placer_bateau(self, classplateau,boat):
        plateau = classplateau.plateau
        coordx= boat.head_coord[1]
        coordy= boat.head_coord[0]
        taille = boat.size
        orientation = boat.orientation
        try:
            for i in range(taille): ## Verif du placement
                if orientation == 'horizontal' and plateau[coordy][coordx+i]in ('1','2'):
                    raise Exception(" Placement impossible ")
                elif orientation == 'vertical'  and plateau[coordy+i][coordx] in ('1','2'):
                    raise Exception(" Placement impossible ")
            ## Placement
            for i in range(taille):
                if orientation == 'horizontal':
                    plateau[coordy][coordx+i] = '1'
                elif orientation == 'vertical':
                     plateau[coordy+i][coordx] = '1'   
            classplateau.list_bateau.append(boat)
            return True
        except Exception as e:
            print(str(e)+' Placement impossible')
            return False
                              
#        
#pla = Plateau(10)
#adm = Adminstrateur('non')
#adm.placer_bateau(pla, Bateau('grand','horizontal',(1,1)))
#pla.display()
#joueur = Joueur('max')
#joueur.lancer_tir(pla,(1,1))
#pla.display()
#joueur.lancer_tir(pla,(1,1))
#joueur.lancer_tir(pla,(1,2))
#joueur.lancer_tir(pla,(1,4))
#joueur.lancer_tir(pla,(1,5))
#joueur.lancer_tir(pla,(1,6))
#pla.display()
#joueur.lancer_tir(pla,(1,7))
#joueur.lancer_tir(pla,(1,9))
#joueur.lancer_tir(pla,(1,8))
#joueur.lancer_tir(pla,(1,3))
#pla.display()
#        
#def main():    
#    board = Plateau(8)
#    print(board.display())
#    print(board.display_bateau_touche())
#