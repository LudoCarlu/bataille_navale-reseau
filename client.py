import socket
from Game import *

hote = 'localhost'
port = 2018

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))


msg_a_envoyer = b""
"""
while msg_a_envoyer != b"fin":
    print('Login :')
    msg_a_envoyer = input("> ")
    if msg_a_envoyer == 'Admin':
        Adminstrateur('toto')
        msg_a_envoyer='logina_'+msg_a_envoyer
    else:
        Joueur('toto')
        msg_a_envoyer='loginj_'+msg_a_envoyer
    msg_a_envoyer = msg_a_envoyer.encode()
    connexion_avec_serveur.send(msg_a_envoyer)
    print('Mdp :')
    msg_a_envoyer = input("> ")
    msg_a_envoyer = msg_a_envoyer.encode()
    connexion_avec_serveur.send(msg_a_envoyer)
    # Peut planter si vous tapez des caractères spéciaux
    msg_a_envoyer = input("> ")
    msg_a_envoyer = msg_a_envoyer.encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)
    msg_recu = connexion_avec_serveur.recv(1024)
    print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents
"""

"""
Dans les envoi de donner {code, data}

login_admin : (login, mdp)
login_joueur : (login, mdp)

"""
a_envoyer = ""
data = ""
code = ""

print("Authentifiez vous :")
print("Login :", end =" ")
login = input()
print("Password :", end=" ")
mdp = input()

if login  == 'admin':
    code = "login_admin"
    data = (login,mdp)
    
else:
    code = "login_joueur"
    data = (login, mdp)

a_envoyer = code + ';' + str(data)
#Envoyer code 
connexion_avec_serveur.send(a_envoyer.encode())

reponse_login = connexion_avec_serveur.recv(1024)
print(repr(reponse_login))
    
    
print("Fermeture de la connexion")
connexion_avec_serveur.close()
