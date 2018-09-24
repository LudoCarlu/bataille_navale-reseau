#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:38:43 2018

@author: ludoviccarlu
"""

import socket
import select
import queue
import numpy as np, pandas as pd
import game

hote = ''
port = 2018

users = pd.read_csv("users.csv")

serveur_actif = True
admin_present = False

#Objets du jeu
adm = None
plateau = None


code_transcription = {
        "login_admin" : ["Authentification successfull", "Authentification failed"],
        "login" : ["Authentification successfull", "Authentification failed"],
        'logina': ('Mot de passe :','login()'),
        'loginj': ('Mot de passe','login()'),
        'supprimera': ('Quel client à supprimer ?','supprimerclient'),
        'jouerj': ('?','lancer_tir'),
        }

code_retour_au_client = {
        "authentification_reussie" : "authentification_reussie;Authentification reussie ! Bienvenue ",
        "authentification_admin" : "authentification_admin;Authentification reussie !",
        "admin_deja_present" : "admin_deja_present;L'administrateur est déjà connecté",
        "admin_absent" : "erreur_presence_admin;Erreur : Aucun administrateur connecté", 
        "erreur_authentification" : ["erreur_authentification;Erreur : Login incorrect", "erreur_authentification;Erreur : Mot de passe incorrect"],
        "initialisation" : "initialisation;Plateau initialisé"
        }

## Fonctions

def authentification(login, password):
    
    if login == "admin" and admin_present == False:
        for idx, row in users.iterrows():
            if row["login"] == "admin":
                if row["mdp"] == password:
                    return code_retour_au_client["authentification_admin"] + ";" + row['role']
            else :
                return code_retour_au_client["erreur_authentification"][1]
    
    elif login == "admin" and admin_present == True:
        return code_retour_au_client["admin_deja_present"]
    #Test si admin ou non
    else: 
        if admin_present:
            for idx, row in users.iterrows() :
                if row['login'] == login:
                    if row['mdp'] == password:                
                        return code_retour_au_client["authentification_reussie"] + ";" + row['role']
                    else:
                        return code_retour_au_client["erreur_authentification"][1]
            return code_retour_au_client["erreur_authentification"][0]
        else:
            return code_retour_au_client["admin_absent"]
  

## Code serveur
            
connexion_du_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_du_serveur.setblocking(0)
connexion_du_serveur.bind((hote, port))
print("socket is binded to %s" %(port))
connexion_du_serveur.listen(15) #Serveur écoute jusqu'à 3 connexions
print("socket is listening")

#inputs = liste de toutes les connexions
inputs = [connexion_du_serveur]
outputs = []
queue_des_messages = {}
connexion_admin  = None
demande_connexion_admin = []

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
            message_du_client_bytes = connexion.recv(1024)
            
            if message_du_client_bytes:
                
                message_du_client_str = message_du_client_bytes.decode()
                message = message_du_client_str.split(";")
                
                print(adresse_du_client[0],":",adresse_du_client[1])
                print("Code :",message[0],"\nRequest :", message[1])
                
                if message[0] == "authentification":
                    retour = eval(message[1]) #Appel authentification(login,password)
                    
                    if retour.split(";")[0] == "authentification_admin":
                        admin_present = True
                        connexion_admin = connexion
                        print("ADMIN : ", adresse_du_client[0],":",adresse_du_client[1])
                        adm = game.Administrateur(retour.split(";")[2])
                    
                    queue_des_messages[connexion].put(retour.encode())
                
                if message[0] == "initialisation":
                    plateau = eval(message[1]) #Initialisation du plateau
                    print(plateau)
                    queue_des_messages[connexion].put(code_retour_au_client["initialisation"].encode())
                    
                if message[0] == "demande_affichage_plateau":
                    retour = ""
                    if plateau is not None:
                        retour = plateau.afficher_plateau()
                    
                    queue_des_messages[connexion].put(retour.encode())
                    
                if message[0] == "creation_bateau":
                    print()
                
                
                if message[0] == "deconnexion":
                    
                    if connexion is connexion_admin:
                        connexion_admin = None
                        admin_present = False
                    #Fermer la connexion
                    exceptional.append(connexion)
                
                if connexion not in outputs:
                    outputs.append(connexion)
            
            else:
                if connexion in outputs:
                    outputs.remove(connexion)
                inputs.remove(connexion)
                connexion.close()
                del queue_des_messages[connexion]

    #Section de l'envoie de message aux clients    
    
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
            outputs.remove(connexion)
        
        connexion.close()
        del queue_des_messages[connexion]
        
        print("VERBOSE DECONNEXION")
        print("inputs", inputs)
        print("outputs", outputs)
        print("exceptional", exceptional)
        exceptional.remove(connexion)


            
    
