import socket
import time
import select
import queue
import UI_Admin as ui_admin
import UI_Connexion as iu_conn
from UI_Client import UI_Client
from tkinter import messagebox
import tkinter as tk

hote = 'localhost'
port = 2013


def envoyer_appel_fonction(code, fonction_avec_args):
    to_send = code + ";" + str(fonction_avec_args)
    connexion_avec_serveur.send(to_send.encode())


def decode_retour_serveur(message_bytes):
    message_str = message_bytes.decode("utf-8")
    retour = message_str.split(";")
    return retour


def initialisation_du_plateau(taille):
    code = "initialisation"
    data = "game.Plateau" + "(" + str(taille_plateau) + ")"
    envoyer_appel_fonction(code, data)
    reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
    
    return reponse;


def demande_affichage_plateau():
    envoyer_appel_fonction("demande_affichage_plateau","")
    plateau = decode_retour_serveur(connexion_avec_serveur.recv(1024))
    
    return "".join(plateau)


def authentification(login, mdp, nombre_tentative):

    role = ""
    code = "authentification"
    data = "authentification" + str((login, mdp))

    envoyer_appel_fonction(code, data)
    reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
    code_retour = reponse[0]

    try:
        message = reponse[1]
        print(message)

    except Exception as e:
        print(e)

    if code_retour == "authentification_reussie" or code_retour == "authentification_admin":
        print("Role:",reponse[2])
        role = reponse[2]
        print(message)

    elif code_retour == "erreur_authentification":
        print(message + "\nRecommencez : " + str((3-nombre_tentative)) + "restantes")

    elif code_retour == "admin_absent" or code_retour == "admin_deja_present":
        print(message+'\nFermeture de la connexion')
        envoyer_appel_fonction("deconnexion","Deconnexion")
        time.sleep(2)
        connexion_avec_serveur.close()

    if nombre_tentative == 3:

        print("Erreur", "3 tentatives échouées\nFermeture de la connexion")
        envoyer_appel_fonction("deconnexion","Deconnexion")
        time.sleep(2)
        connexion_avec_serveur.close()

    return code_retour, role


## DEBUT SEQUENCE CLIENT ##
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

"""
Envoie de donnée code; data
Retour de donnée code; reponse
"""

data = ""
code = ""
code_retour = ""
role = ""
login = ""

#Authentification
compteur_tentative = 0
while (
       (code_retour != "authentification_reussie" 
       and code_retour != "authentification_admin"
       and code_retour != "admin_absent"
       and code_retour != "admin_deja_present"
       ) 
       and compteur_tentative <3
       ):

    login = input("Entrez votre login : ")
    mdp = input("Entrez votre mot de passe : ")

    code_retour, role = authentification(login, mdp, compteur_tentative)
    compteur_tentative += 1


print("Suite du scénario")

try:

    if role == "admin":

        ## PART 1 INITIALISATION DE LA PARTIE

        taille_plateau = 0

        #Création du plateau
        taille_plateau = ui_admin.fenetre_choix_dimensions()

        reponse = initialisation_du_plateau(taille_plateau)
        code_retour = reponse[0]
        message = reponse[1]
        print("code:",code_retour, "message:", message)
        print(message)
        print()

        print("=== MENU CREATION DE BATEAU ===")
        print("".join(demande_affichage_plateau()))
        print()

        # bateau : type_bateau ,orientation, head_coord
        # placer_bateau(self, classplateau,boat)
        # Création des bateaux

        ajouter_bateau = True
        nb_de_bateau_max = 3
        i=0
        ini_plateau=""
        while i < nb_de_bateau_max:
            type_bateau, orientation, x, y = ui_admin.fenetre_placement(taille_plateau,ini_plateau)
            print(type_bateau,orientation,x,y)

            code = "creation_bateau"
            data = "adm.placer_bateau(plateau,game.Bateau('" + type_bateau + "','" + orientation + "',(" + str(x) + "," + str(y) + ")))"
            i = i + 1
            print("code :" + code + " data : " + data)
            envoyer_appel_fonction(code, data)
            print()
            reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
            code_retour = reponse[0]

            if len(reponse) == 2:
                if reponse[1] == "placement_impossible":
                    print("Placement impossible")
                    nb_de_bateau_max += 1

            print(code_retour)
            print(message)
            ini_plateau=code_retour

        # PART 2 GESTION DES CONNEXIONS

        envoyer_appel_fonction("liste_joueurs_en_attente", "")
        reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
        code_retour = reponse[0]
        print(code_retour)

        list_accept = ui_admin.fenetre_choix_clients(code_retour)
        time.sleep(0.5)
        envoyer_appel_fonction("accepter_joueur_ui", list_accept)
        time.sleep(0.5)

        envoyer_appel_fonction("debut_partie", "La partie commence !")

        while decode_retour_serveur(connexion_avec_serveur.recv(1024))[0] != "fin_partie":
            print(message + '\nFermeture de la connexion')
            envoyer_appel_fonction("deconnexion", "Deconnexion")

    if role == "joueur":
        print("Veuillez attendre la décision de l'administrateur")
        inputs = [connexion_avec_serveur]
        outputs = []
        queue_des_messages = {}
        queue_des_messages[connexion_avec_serveur] = queue.Queue()

        while connexion_avec_serveur:

            readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.05)

            for connexion in readable:

                message_du_serveur_bytes = connexion_avec_serveur.recv(1024)

                if message_du_serveur_bytes:

                    message = decode_retour_serveur(message_du_serveur_bytes)
                    code_retour = message[0]
                    data = message[1]

                    if code_retour == "accepter":
                        print(data)
                        print()

                    if code_retour == "refuser":
                        print(data)
                        print()
                        envoyer_appel_fonction("deconnexion", "Deconnexion")
                        print("Fermeture de la connexion")
                        connexion_avec_serveur.close()

                    if code_retour == "a_toi":
                        print(data)
                        print()
                        print("=====================")
                        print("".join(message[2]))
                        print("=====================")
                        print()
                        condition = True
                        flag = 0
                        while condition:
                            x = input("Ligne : ")
                            y = input("Colonne  : ")
                            size = len(message[2].split("\n"))
                            print("taille plateau " +str(size))
                            if int(x) < 0 or int(x) >= int(size):
                                print(x)
                                flag = 1
                            if int(y) < 0 or int(y) >= int(size):
                                flag = 1
                                print(y)

                            if flag == 1:
                                condition = True
                                print("Coordonnées incorrects")

                            else:
                                condition=False

                        code = "lancement_tir;"
                        fct = "j.lancer_tir(plateau, (" + str(x) + "," + str(y) + "))"
                        to_send = code + fct
                        queue_des_messages[connexion].put(to_send.encode())
                        # print("".join(demande_affichage_plateau()))

                    if code_retour == "pas_toi":
                        print(data)
                        print()

                    if code_retour == "resultat_tir":
                        to_send = "au_suivant;" + ""
                        queue_des_messages[connexion].put(to_send.encode())
                        print("=====================")
                        print("".join(message[2]))
                        print(data)
                        print()

                    if code_retour == "fin_partie":
                        print(data)
                        print()
                        envoyer_appel_fonction("deconnexion", "Deconnexion")
                        print("Fermeture de la connexion")

                    if connexion not in outputs:
                        outputs.append(connexion)

                else:

                    exceptional.append(connexion)

            for connexion in writable:
                try:
                    message_suivant = queue_des_messages[connexion].get_nowait()
                    # print("Message suivant : " + str(message_suivant))

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
                # print("VERBOSE EXCEPTIONNAL")
                # print("inputs", inputs)
                # print("outputs", outputs)
                # print("exceptional", exceptional)
                exceptional.remove(connexion)

                exceptional.remove(connexion)






except Exception as e:
    print(e)
    connexion_avec_serveur.close()




