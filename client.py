import socket
import game

hote = 'localhost'
port = 2018



def envoyer_appel_fonction(code, fonction_avec_args):
    to_send = code + ";" + str(fonction_avec_args)
    connexion_avec_serveur.send(to_send.encode())

def decode_retour_serveur(message_bytes):
    message_str = message_bytes.decode()
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
    
    return plateau

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
    message = reponse[1]
    
    if code_retour == "authentification_reussie" or code_retour == "authentification_admin":
        role = reponse[2]
        print("Role:",role)
        
    print(message)
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
    print(demande_affichage_plateau())
    print()    
    
    """
    #bateau : type_bateau ,orientation, head_coord
    #placer_bateau(self, classplateau,boat)
    #Création des bateaux
    ajouter_bateau = True
    nb_de_bateau_max = 3
    
    while i < nb_de_bateau_max:

        print("Quel type de bateau voulez vous placer ?")
        type_bateau = int(input("1 : Petit\n2 : Moyen\n3 : Grand"))
        orientation = int(input("1 : Horizontale\n2 :Verticale"))
        x = input("Coordonnée X de la tête: ")
        y = input("Coordonnée Y de la tête: ")
        
        if type_bateau == 1:
            type_bateau = "petit"
        elif type_tableau == 2:
            type_bateau = "moyen"
        elif type_bateau == 3:
            type_bateau = "grand"
        
        if orientation == 1:
            orientation = "horizontale"
        elif orientation == 2:
            orientation = "verticale"
               
        code = "creation_bateau"
        data = "adm.placer_bateau(plateau,Bateau("+type_bateau+","+orientation+",("+x+","+y+")"
        
        print()
    """
    ## PART 2 GESTION DES CONNEXIONS    

if role == "joueur":
    print("Wait for entrance")
    retour = decode_retour_serveur(message_bytes)




