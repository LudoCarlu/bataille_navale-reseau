import socket
import time
import select
import queue
import UI_Admin as ui_admin
import UI_Connexion as iu_conn
from tkinter import messagebox

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


def authentification(login, mdp, nombre_tentative, fenetre):

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
        messagebox.showinfo("Connexion", "Connexion reussie")
        fenetre.destroy()


    elif code_retour == "erreur_authentification":
        fenetre.withdraw()
        messagebox.showerror("Erreur", message + "\nRecommencez : " + str((3-nombre_tentative)) + "restantes")
        fenetre.destroy()


    elif code_retour == "admin_absent" or code_retour == "admin_deja_present":
        #fenetre.withdraw()
        messagebox.showerror("Erreur", message+'\nFermeture de la connexion')
        envoyer_appel_fonction("deconnexion","Deconnexion")
        time.sleep(2)
        print("Fermeture de la connexion")
        connexion_avec_serveur.close()

    if nombre_tentative == 3:
        print()
        #fenetre.withdraw()
        messagebox.showerror("Erreur", "3 tentatives échouées\nFermeture de la connexion")
        envoyer_appel_fonction("deconnexion","Deconnexion")
        time.sleep(2)
        print("Fermeture de la connexion")
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

    login, mdp, fenetre = iu_conn.fenetre_connexion()
    code_retour, role = authentification(login, mdp, compteur_tentative, fenetre)
    compteur_tentative += 1

print("Wait 3s")
time.sleep(3)

print("Suite du scénario")
try:

    if role == "admin":

        ## PART 1 INITIALISATION DE LA PARTIE

        commande = 0
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


        #bateau : type_bateau ,orientation, head_coord
        #placer_bateau(self, classplateau,boat)
        #Création des bateaux
        ajouter_bateau = True
        nb_de_bateau_max = 2
        i=0
        while i < nb_de_bateau_max:

            type_bateau, orientation, x, y = ui_admin.fenetre_placement(taille_plateau)
            print(type_bateau,orientation,x,y)

            #game.Bateau(type_bateau,orientation,(x,y))
            code = "creation_bateau"
            data = "adm.placer_bateau(plateau,game.Bateau('" + type_bateau + "','" + orientation + "',(" + str(x) + "," + str(y) + ")))"
            #data = "adm.placer_bateau(plateau,game.Bateau(" + type_bateau + "," + orientation + ",(" + str(x) + "," + str(y) + ")))"

            i = i + 1
            print("code :" + code + " data : " + data)
            envoyer_appel_fonction(code, data)
            print()
            reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
            code_retour = reponse[0]
            print(code_retour)
            print(message)

            #print('Erreur lors de la création de vos paramètres bateau')


        ## PART 2 GESTION DES CONNEXIONS

        nb_de_joueur = int(input("Combien de joueur voulez vous ? "))
        envoyer_appel_fonction("nb_de_joueur",str(nb_de_joueur))
        reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
        code_retour = reponse[0]
        print(code_retour)



        stop = False
        i = 0
        while i < nb_de_joueur and stop is False:
            envoyer_appel_fonction("liste_joueurs_en_attente", "")
            reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
            code_retour = reponse[0]
            print(code_retour)
            time.sleep(1)
            idx = str(input("Joueur accepté (Index) ? ou Stop\n"))
            if idx.lower() is "stop":
                envoyer_appel_fonction("refuser_joueur", "")
                stop = True
            else:
                envoyer_appel_fonction("accepter_joueur", idx)
            time.sleep(1)
            i += 1

        envoyer_appel_fonction("refuser_joueur", "") #Vide le tableau des joueurs en attente
        time.sleep(0.5)

        envoyer_appel_fonction("debut_partie", "La partie commence !")

        while connexion_avec_serveur:
            pass

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

                    if code_retour == "refuser":
                        print(data)
                        envoyer_appel_fonction("deconnexion", "Deconnexion")
                        print("Fermeture de la connexion")
                        connexion_avec_serveur.close()

                    if code_retour == "a_toi":
                        print(data)
                        x = input("Coord X : ")
                        y = input("Coord Y : ")
                        code = "lancement_tir;"
                        fct = "j.lancer_tir(plateau, (" + str(x) +","+ str(y) + "))"
                        to_send = code + fct
                        queue_des_messages[connexion].put(to_send.encode())
                        # print("".join(demande_affichage_plateau()))

                    if code_retour == "pas_toi":
                        print(data)

                    if code_retour == "resultat_tir":
                        print(data)
                        to_send = "au_suivant;" + ""
                        queue_des_messages[connexion].put(to_send.encode())

                    if code_retour == "fin_de_partie":
                        # Score : X, Vous avez gagné ou perdu ou nul
                        print(data)

                    if connexion not in outputs:
                        outputs.append(connexion)

                else:
                    """
                    if connexion in outputs:
                        outputs.remove(connexion)
                    inputs.remove(connexion)
                    connexion.close()
                    del queue_des_messages[connexion]
                    """
                    exceptional.append(connexion)

            for connexion in writable:
                try:
                    message_suivant = queue_des_messages[connexion].get_nowait()
                    print("Message suivant : " + str(message_suivant))

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
                print("VERBOSE EXCEPTIONNAL")
                print("inputs", inputs)
                print("outputs", outputs)
                print("exceptional", exceptional)
                exceptional.remove(connexion)

                exceptional.remove(connexion)






except Exception as e:
    print(e)
    connexion_avec_serveur.close()




