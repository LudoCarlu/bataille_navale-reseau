#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:38:43 2018

@author: ludoviccarlu
"""

import socket
import threading
import select
import time

hote = ''
port = 2018
        ## message_description[messageclient] ->
        # message_description[messageclient][0] -> Réponse du serveur
        # message_description[messageclient][1] -> Fonction a appeler
message_description_server = { 
        'logina': ('Mot de passe :','login()'),
        'loginj': ('Mot de passe','login()'),
        'supprimera': ('Quel client à supprimer ?','supprimerclient'),
        'jouerj': ('?','lancer_tir'),
        }

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))


    def get_clientsocket(self):
        return self.clientsocket
    """
    def set_x(self, x):
        self.__x = x
    """
    
    def run(self): 
   
        print("Connexion de %s %s" % (self.ip, self.port, ))

        #r = self.clientsocket.recv(2048)
        #print("Ouverture du fichier: ", r, "...")
        #fp = open(r, 'rb')
        #self.clientsocket.send(fp.read())

        #print("Client déconnecté...")
        #self.clientsocket.close()
        

##########
        
serveur_actif = True
clients_connectes = []

connexion_du_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_du_serveur.bind((hote, port))
print("socket is binded to %s" %(port))
connexion_du_serveur.listen(3) #Serveur écoute jusqu'à 3 connexions
print( "socket is listening")


while serveur_actif:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms

    connexions_demandees, wlist, xlist = select.select([connexion_du_serveur], [], [], 0.05)
    
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        print("Got connexion from %s : %s" % (infos_connexion[0], infos_connexion[1]))
        # On ajoute le thread contenant le socket connecté à la liste des clients
        newthread = ClientThread(infos_connexion[0], infos_connexion[1], connexion_avec_client)
        newthread.start()
        clients_connectes.append(newthread.get_clientsocket())
    
    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    
    clients_a_lire = []
    try:
        """
        rlist: wait until ready for readingvc
        wlist: wait until ready for writing
        xlist: wait for an “exceptional condition”
        """
        #client a lire : rlist
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass
    else:
        # On parcourt la liste des clients à lire
        for client in clients_a_lire:
            # Client est de type socket
            msg_recu = client.recv(1024)
            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode()
            print("Reçu {}".format(msg_recu))
            client.send(b"5 / 5")
            
            if msg_recu == "fin":
                print("Client s'est déconnecté")
                client.close()
                
                
"""
print("Fermeture des connexions")
for client in clients_connectes:
    client.close()
"""
connexion_principale.close()