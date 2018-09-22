#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:38:43 2018

@author: ludoviccarlu
"""

import socket
import select
import time
import sys
import queue

hote = ''
port = 2018
        ## message_description[messageclient] ->
        # message_description[messageclient][0] -> Réponse du serveur
        # message_description[messageclient][1] -> Fonction a appeler
code_transcription = {
        "login_admin" : ["Authentification successfull", "Authentification failed"],
        "login_joueur" : ["Authentification successfull", "Authentification failed"],
        'logina': ('Mot de passe :','login()'),
        'loginj': ('Mot de passe','login()'),
        'supprimera': ('Quel client à supprimer ?','supprimerclient'),
        'jouerj': ('?','lancer_tir'),
        }

        
connexion_du_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_du_serveur.setblocking(0)
connexion_du_serveur.bind((hote, port))
print("socket is binded to %s" %(port))
connexion_du_serveur.listen(3) #Serveur écoute jusqu'à 3 connexions
print( "socket is listening")

#inputs = liste de toutes les connexions
inputs = [connexion_du_serveur]
outputs = []
queue_des_messages = {}

serveur_actif = True

while inputs:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion du serveur en lecture
    # On attend maximum 50ms

    readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.05)
    
    for connexion in readable:
        
        if connexion is connexion_du_serveur: #s est le serveur
            
            connexion_avec_client, adresse_du_client = connexion.accept()
            connexion.setblocking(0)
            print("Connexion de %s : %s" % (adresse_du_client[0], adresse_du_client[1]))
            
            inputs.append(connexion_avec_client)
            #On crée une liste pour les messages de ce client
            queue_des_messages[connexion_avec_client] = queue.Queue()
            
        else:
            message_du_client = connexion.recv(1024)
            print(adresse_du_client[0],":",message_du_client.decode())
            
            if message_du_client:
                queue_des_messages[connexion].put(message_du_client)
                if connexion not in outputs:
                    outputs.append(connexion)
            
            else:
                if connexion in outputs:
                    outputs.remove(connexion)
                inputs.remove(connexion)
                connexion.close()
                del queue_des_messages[connexion]
            
    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    
    for connexion in writable:
    
        try:
            message_suivant = queue_des_messages[connexion].get_nowait()
            
        except queue.Empty:
            outputs.remove(connexion)
            
        else:
            connexion.send(message_suivant)
    
    
    for connexion in exceptional:
        
        inputs.remove(connexion)
        
        if connexion in outputs:
            outputs.remove(s)
        
        connexion.close()
        del queue_des_messages[connexion]
        

