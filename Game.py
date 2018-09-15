#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 23:29:41 2018

@author: ludoviccarlu
"""

class Plateau:
    
    def __init__(self, size):
        self.plateau = []
        self.size = size
        
        for i in range (size):
            self.plateau.append([0] *size)
        
        
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
                    print('0', end = ' ')
            print()


class Bateau:
    
    '''
    state : 2 touché
    state : 1 non touché
    state : 3 coulé
    size : taille du bateau
    coord = [[x,y],[x,y], ...]
    '''
    
    def __init__(self, size, coord, state):
        print("bateau")
        
        
class Joueur:
    
    def __init__(self, name, is_master_player):
        print(self.name, self.is_master_player)
        
    def creer_bateau(self, size, coord):
        print()
    
        
def main():    
    board = Plateau(8)
    print(board.display())
    print(board.display_bateau_touche())

main()