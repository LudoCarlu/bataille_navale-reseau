#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:38:43 2018

@author: ludoviccarlu
"""

import socket
import select
import queue
import pandas as pd
import Game as game
import time

hote = ''
global port
port = 2013

users = pd.read_csv("users.csv")

serveur_actif = True
admin_present = False

# Objets du jeu
adm = None
plateau = None
joueurs = []
joueurs_en_attente = []
index_joueur_qui_joue = 0


code_retour_au_client = {
    "authentification_reussie": "authentification_reussie;Authentification reussie ! Bienvenue ",
    "authentification_admin": "authentification_admin;Authentification reussie !",
    "admin_deja_present": "admin_deja_present;L'administrateur est déjà connecté",
    "admin_absent": "admin_absent;Erreur : Aucun administrateur connecté",
    "erreur_authentification": ["erreur_authentification;Erreur : Login incorrect",
                                "erreur_authentification;Erreur : Mot de passe incorrect"],
    "initialisation": "initialisation;Plateau initialisé",
    "a_toi":"a_toi;C'est ton tour de jouer !",
    "pas_toi":"pas_toi;Un autre joueur joue ! Attendez !"
}


## Fonctions

def authentification(login, password):
    if login == "admin" and adm is None:
        for idx, row in users.iterrows():
            if row["login"] == "admin":
                if row["mdp"] == password:
                    return code_retour_au_client["authentification_admin"] + ";" + row['role'], login
            else:
                return code_retour_au_client["erreur_authentification"][1], "echec"

    elif login == "admin" and adm is not None:
        return code_retour_au_client["admin_deja_present"],"echec"
    # Test si admin ou non
    else:
        if adm is not None:
            for idx, row in users.iterrows():
                if row['login'] == login:
                    if row['mdp'] == password:
                        return code_retour_au_client["authentification_reussie"] + ";" + row['role'], login
                    else:
                        return code_retour_au_client["erreur_authentification"][1], "echec"
            return code_retour_au_client["erreur_authentification"][0], "echec"
        else:
            return code_retour_au_client["admin_absent"], "echec"


## Code serveur

connexion_du_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_du_serveur.setblocking(0)
connexion_du_serveur.bind((hote, port))
print("socket is binded to %s" % (port))
connexion_du_serveur.listen(15)  # Serveur écoute jusqu'à 15 connexions
print("socket is listening")
print()

# inputs = liste de toutes les connexions
inputs = [connexion_du_serveur]
outputs = []
queue_des_messages = {}

while inputs:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion du serveur en lecture
    # On attend maximum 50ms

    readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.05)

    for connexion in readable:

        if connexion is connexion_du_serveur:  # s est le serveur

            connexion_avec_client, adresse_du_client = connexion.accept()
            connexion.setblocking(0)
            print("Connexion de %s : %s" % (adresse_du_client[0], adresse_du_client[1]))
            print()

            inputs.append(connexion_avec_client)
            # On crée une liste pour les messages de ce client
            queue_des_messages[connexion_avec_client] = queue.Queue()

        else :
            message_du_client_bytes = connexion.recv(1024)

            if message_du_client_bytes:

                message_du_client_str = message_du_client_bytes.decode()
                message = message_du_client_str.split(";")

                print(adresse_du_client[0], ":", adresse_du_client[1])
                print("Code :", message[0], "\nRequest :", message[1],'\n')
                print()

                try:

                    if message[0] == "authentification":
                        retour, name = eval(message[1])  # Appel authentification(login,password)

                        if name == "admin":
                            adm = game.Administrateur(name, connexion)
                            admin_present = True
                            print("ADMIN : ", adresse_du_client[0], ":", adresse_du_client[1])

                        elif (name != "admin") and (name is not "echec"):
                            joueurs_en_attente.append(game.Joueur(name,connexion))

                        queue_des_messages[connexion].put(retour.encode())

                    if message[0] == "initialisation":
                        plateau = eval(message[1])  # Initialisation du plateau
                        queue_des_messages[connexion].put(code_retour_au_client["initialisation"].encode())

                    if message[0] == "demande_affichage_plateau":
                        retour = ""
                        if plateau is not None:
                            retour = plateau.afficher_plateau()

                        queue_des_messages[connexion].put(retour.encode())

                    if message[0] == "creation_bateau":
                        try:
                            est_place = eval(message[1])
                            retour = plateau.afficher_plateau()

                            if est_place is False:
                                retour = retour + ";" + "placement_impossible"

                        except Exception as e:
                            retour = 'Erreur ! Placement impossible'
                        queue_des_messages[connexion].put(retour.encode())
                        print()

                    if message[0] == "nb_de_joueur":
                        retour = "Il y a " + str(len(joueurs_en_attente)) + " qui attendent votre approbation"
                        queue_des_messages[connexion].put(retour.encode())

                    if message[0] == "liste_joueurs_en_attente":
                        retour = ""
                        i = 0
                        for j in joueurs_en_attente:
                            retour += str(i) + ":" + j.get_name()
                            if i != len(joueurs_en_attente)-1:
                                retour += ","
                            i += 1

                        if len(joueurs_en_attente) == 0:
                            retour = "None"

                        queue_des_messages[connexion].put(retour.encode())

                    if message[0] == "accepter_joueur_ui":
                        idx_joueurs_acceptés = message[1].split(",")

                        for j in joueurs_en_attente:

                            if str(joueurs_en_attente.index(j)) in idx_joueurs_acceptés:
                                joueurs.append(j)
                                to_send = "accepter;Vous avez été selectionné par l'administrateur\nA vous de jouer " + j.get_name() + "!"
                                queue_des_messages[j.get_connexion()].put(to_send.encode())
                                outputs.append(j.get_connexion())

                        time.sleep(0.3)

                        for j in joueurs_en_attente:
                            if j not in joueurs:
                                to_send = "refuser;Vous n'avez pas été selectionné par l'administrateur"
                                queue_des_messages[j.get_connexion()].put(to_send.encode())
                                joueurs_en_attente.remove(j)
                                outputs.append(j.get_connexion())
                            else:
                                joueurs_en_attente.remove(j)

                    if message[0] == "accepter_joueur":
                        idx = int(message[1])
                        j = joueurs_en_attente[idx]
                        joueurs.append(j)
                        to_send = "accepter;Vous avez été selectionné par l'administrateur\nA vous de jouer "+j.get_name()+"!"
                        queue_des_messages[j.get_connexion()].put(to_send.encode())
                        joueurs_en_attente.remove(j)
                        outputs.append(j.get_connexion())

                    if message[0] == "refuser_joueur":
                        if len(joueurs_en_attente) > 0:
                            for j in joueurs_en_attente:
                                to_send = "refuser;Vous n'avez pas été selectionné par l'administrateur"
                                queue_des_messages[j.get_connexion()].put(to_send.encode())
                                joueurs_en_attente.remove(j)
                                outputs.append(j.get_connexion())
                                #La demande de deconnexion se fait ensuite côté client

                    # Envoyer par l'admin
                    if message[0] == "debut_partie":

                        # On donne le tour au premier arrivée
                        joueur1 = joueurs[0]
                        joueur1.set_tour(True)
                        index_joueur_qui_joue = 0

                        to_send = code_retour_au_client["a_toi"]+";"+plateau.afficher_plateau_client()
                        queue_des_messages[joueur1.get_connexion()].put(to_send.encode())
                        outputs.append(joueur1.get_connexion())

                        time.sleep(1)
                        to_send = code_retour_au_client["pas_toi"]
                        for j in joueurs:
                            if j is not joueur1:
                                j.set_tour(False)
                                queue_des_messages[j.get_connexion()].put(to_send.encode())
                                outputs.append(j.get_connexion())

                    # Envoyer par un joueur
                    if message[0] == "lancement_tir":
                        # On lance lancer_tir(pla, coord)
                        for j in joueurs:
                            if connexion is j.get_connexion() and j.get_tour() is True:
                                result = eval(message[1])
                                retour = "resultat_tir;" + result +";"+plateau.afficher_plateau_client()

                                if result == 'Touché !':
                                    j.add_point(1)
                                if result == 'Coulé !':
                                    j.add_point(3)

                                queue_des_messages[j.get_connexion()].put(retour.encode())
                                outputs.append(j.get_connexion())

                            else:
                                retour = code_retour_au_client["pas_toi"]
                                queue_des_messages[j.get_connexion()].put(retour.encode())
                                outputs.append(j.get_connexion())

                        if plateau.is_partie_finie():
                            code = "fin_partie"
                            message_for_admin = "La partie est terminée"
                            to_send = code + ";" + message_for_admin

                            #Envoie message à l'admin
                            queue_des_messages[adm.get_connexion()].put(to_send.encode())
                            outputs.append(adm.get_connexion())

                            for j in joueurs:
                                message_for_joueur = "La partie est terminée\nVotre score est : " + str(j.get_score())
                                to_send = code + ";" + message_for_joueur
                                queue_des_messages[j.get_connexion()].put(to_send.encode())
                                outputs.append(j.get_connexion())

                    # Renvoyer par le client qui vient d'avoir le résultat de son tir
                    if message[0] == "au_suivant":
                        for j in joueurs:
                            idx = joueurs.index(j)

                            # Le joueur venant de jouer
                            if j.get_tour() is True:
                                j.set_tour(False)

                                # Si c'était le dernier on repart au début
                                if idx == len(joueurs) - 1:
                                    index_joueur_qui_joue = 0
                                    break
                                # Sinon increment pour le suivant
                                else:
                                    index_joueur_qui_joue += 1
                                    break

                        joueurs[index_joueur_qui_joue].set_tour(True)
                        to_send = code_retour_au_client["a_toi"]+";"+plateau.afficher_plateau_client()
                        queue_des_messages[joueurs[index_joueur_qui_joue].get_connexion()].put(to_send.encode())
                        outputs.append(joueurs[index_joueur_qui_joue].get_connexion())

                    if message[0] == "deconnexion":

                        # Fermer la connexion
                        exceptional.append(connexion)

                    if connexion not in outputs:
                        outputs.append(connexion)

                except Exception as e:
                    print(e)
                    connexion_du_serveur.close()
            else:

                exceptional.append(connexion)

    # Section de l'envoie de message aux clients

    for connexion in writable:

        try:
            message_suivant = queue_des_messages[connexion].get_nowait()
            print("Envoi serveur vers : " + str(connexion.getpeername()))
            print("Message suivant : " + str(message_suivant))
            print()
            time.sleep(0.3)

        except queue.Empty:
            outputs.remove(connexion)

        else:
            connexion.send(message_suivant)

    # Section des erreurs

    for connexion in exceptional:
        inputs.remove(connexion)

        if connexion in outputs:
            outputs.remove(connexion)

        connexion.close()
        del queue_des_messages[connexion]

        if admin_present:
            if connexion is adm.get_connexion():
                adm = None
                admin_present = False
        else:
            pass

        """
        print("VERBOSE DECONNEXION")
        print("inputs", inputs)
        print("outputs", outputs)
        print("exceptional", exceptional)
        """
        exceptional.remove(connexion)
