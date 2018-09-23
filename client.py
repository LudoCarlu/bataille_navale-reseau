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
    while commande not in(1,2,3):
        print("Menu administrateur")
        print("1: Initialiser le plateau")
        #print("2: Placer des bateaux")
        print("3: Accepter les joueurs")
        commande = int(input("Que souhaitez vous faire ? "))
    return commande


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
    adm = game.Administrateur(login)
    commande = 0
    taille_plateau = 0    
    plateau = None
    commande = menu_admin()
    
    if commande == 1:
        while taille_plateau < 10:
            taille_plateau = int(input("Quelle est la taille de votre plateau? Minimum : 10 \n"))
            print()
        
        code = "initialisation"
        data = "game.Plateau" + "(" + str(taille_plateau) + ")"
        envoyer_appel_fonction(code, data)
        reponse = decode_retour_serveur(connexion_avec_serveur.recv(1024))
        code_retour = reponse[0]
        message = reponse[1]
        print("code:",code_retour, "message:", message)
        print(message)
    
    




