import socket
import game as game
import time
import select
import queue

hote = 'localhost'
port = 2011


def envoyer_appel_fonction(code, fonction_avec_args):
    to_send = code + ";" + str(fonction_avec_args)
    connexion_avec_serveur.send(to_send.encode())

def decode_retour_serveur(message_bytes):
    message_str = message_bytes.decode("utf-8")
    retour = message_str.split(";")
    return retour
   
def menu_admin():
    commande = 0
    while commande not in range(1,5):
        print("Menu administrateur")
        print("1: Initialiser le plateau")
        print("2: Placer des bateaux")
        print("3: Créer un joueur")
        print("4: Accepter les joueurs")
        commande = int(input("Que souhaitez vous faire ? "))
    return commande

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
    
    print("Authentifiez vous :")
    login = input("Login :")
    mdp = input("Password :")
    
    code = "authentification"
    data = "authentification" + str((login,mdp))
    
    envoyer_appel_fonction(code, data)
    reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
    code_retour = reponse[0]
    print(code_retour)
    try:
        message = reponse[1]
        print(message)
    except Exception  as e:
        print(e)
    
    if code_retour == "authentification_reussie" or code_retour == "authentification_admin":
        role = reponse[2]
        print("Role:",role)

    compteur_tentative += 1
    print()

if code_retour == "admin_absent" or code_retour == "admin_deja_present":
    envoyer_appel_fonction("deconnexion","Deconnexion")
    print("Fermeture de la connexion")
    connexion_avec_serveur.close()

if compteur_tentative == 3:
    print("3 tentatives échouées")
    envoyer_appel_fonction("deconnexion","Deconnexion")
    print("Fermeture de la connexion")
    connexion_avec_serveur.close()
    
print("Suite du scénario")
try:

    if role == "admin":

        ## PART 1 INITIALISATION DE LA PARTIE

        commande = 0
        taille_plateau = 0

        #Création du plateau
        while taille_plateau < 10:
            taille_plateau = int(input("Quelle est la taille de votre plateau? Minimum : 10 \n"))
            print()

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
        nb_de_bateau_max = 0
        i=0
        while i < nb_de_bateau_max:

            print("Quel type de bateau voulez vous placer ?")
            type_bateau = int(input("1 : Petit\n2 : Moyen\n3 : Grand\n"))
            orientation = int(input("1 : Horizontale\n2 :Verticale\n"))
            x = input("Coordonnée X de la tête: ")
            y = input("Coordonnée Y de la tête: ")

            if type_bateau == 1:
                type_bateau = "petit"
            elif type_bateau == 2:
                type_bateau = "moyen"
            elif type_bateau == 3:
                type_bateau = "grand"

            if orientation == 1:
                orientation = "horizontale"
            elif orientation == 2:
                orientation = "verticale"

            try:
                game.Bateau(type_bateau,orientation,(x,y))
                code = "creation_bateau"
                data = "adm.placer_bateau(plateau,Bateau('" + type_bateau + "','" + orientation + "',(" + x + "," + y + ")))"
                i = i + 1
                print()
                envoyer_appel_fonction(code, data)
                print()
                reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
                code_retour = reponse[0]
                print(code_retour)
                print(message)
            except:
                print('Erreur lors de la création de vos paramètres bateau')

        """
        reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
        code_retour = reponse[0]
        print(code_retour)
        reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
        code_retour = reponse[0]
        print(code_retour)
        reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
        code_retour = reponse[0]
        print(code_retour)
        """

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

                    print(data)

                    if code_retour is "refuser":
                        envoyer_appel_fonction("deconnexion", "Deconnexion")
                        print("Fermeture de la connexion")
                        connexion_avec_serveur.close()

                    if connexion not in outputs:
                        outputs.append(connexion)

                else:
                    if connexion in outputs:
                        outputs.remove(connexion)
                    inputs.remove(connexion)
                    connexion.close()
                    del queue_des_messages[connexion]

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

                print("VERBOSE DECONNEXION")
                print("inputs", inputs)
                print("outputs", outputs)
                print("exceptional", exceptional)
                exceptional.remove(connexion)




except Exception as e:
    print(e)
    connexion_avec_serveur.close()




