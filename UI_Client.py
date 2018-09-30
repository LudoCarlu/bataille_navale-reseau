from tkinter import *


class UI_Client (Frame):
    def __init__(self, fenetre, initialPlateau, connexion_avec_serveur,**kwargs):
        LabelFrame.__init__(self, fenetre, text="Interface client",
                            borderwidth=6, **kwargs)
        self.score=0
        self.pseudo ="Test"
        self.initialPlateau=initialPlateau
        self.connexion_avec_serveur = connexion_avec_serveur

        self.pack(side=TOP, padx=1, pady=1, expand="yes", fill=BOTH)

        self.labelMessage = LabelFrame(self,text="Messages")
        self.labelMessage.pack(side=RIGHT,expand='yes',fill=Y)
        S = Scrollbar(self.labelMessage)
        S.pack(side=RIGHT, fill=Y)
        self.textMessages = Text(self.labelMessage,height=10)
        self.textMessages.config(yscrollcommand=S.set)
        self.textMessages.pack(side=RIGHT, fill=Y)
        self.textMessages.configure(state='normal')
        self.textMessages.insert(END,"Bonjour, bienvenue "+self.pseudo+" !\n")
        self.textMessages.see(END)
        self.textMessages.configure(state='disabled')

        ## Grid pour placement
        self.tableau_plateau = self.traitementstringPlateau()

        self.actionLabel = LabelFrame(self,text="Mon plateau")
        self.actionLabel.pack(side=BOTTOM,fill=BOTH)
        labelPseudo = Label(self,text="Joueur : "+self.pseudo)
        labelPseudo.pack()
        self.labelScore = Label(self,text="Score : "+str(self.score))
        self.labelScore.pack()

        self.actualiser_plateau()

        fenetre.mainloop()
        code_retour=""

    def traitementstringPlateau(self):
        mon_plateau = self.initialPlateau[:-1].split("\n")
        for i in range(len(mon_plateau)):
            mon_plateau[i] = mon_plateau[i].split(" ")
        return mon_plateau

    def lancement_tir(self, row, col):
        message_du_serveur_bytes = self.connexion_avec_serveur.recv(1024)
        if message_du_serveur_bytes:
            message = message_du_serveur_bytes.decode().split(';')
            code_retour = message[0]
            data = message[1]
            if code_retour == "a_toi":
                print(data)
                x = row
                y = col
                code = "lancement_tir;"
                fct = "j.lancer_tir(plateau, (" + str(x) + "," + str(y) + "))"
                to_send = code + fct
                self.connexion_avec_serveur.send(to_send.encode())

                message_du_serveur_bytes = self.connexion_avec_serveur.recv(1024)
                message = message_du_serveur_bytes.decode().split(';')
                code_retour = message[0]
                data = message[1]


            if code_retour == "pas_toi":
                self.textMessages.configure(state='normal')
                self.textMessages.insert(END, data + "\n")
                self.textMessages.configure(state='disabled')
                self.textMessages.update()

            if code_retour == "resultat_tir":
                print(data)
                to_send = "au_suivant;" + ""
                self.connexion_avec_serveur.send(to_send.encode())
                self.initialPlateau = message[2]
                self.textMessages.configure(state='normal')
                self.textMessages.insert(END, data + "\n")
                self.textMessages.configure(state='disabled')
                self.textMessages.update()

            if code_retour == "fin_de_partie":
                # Score : X, Vous avez gagné ou perdu ou nul
                print(data)

        ## fonction du client/serveur
       # self.etat_du_tir = "touche"
        nouveau_plateau ="~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ T ~ ~ ~\n~ ~ ~ ~ C C C ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n"
        #self.score=1
        ##

        self.tableau_plateau = self.traitementstringPlateau()

        self.actualiser_plateau()

        self.labelScore.config(text="Score : "+str(self.score))

    def actualiser_plateau(self):
        for i in range(len(self.tableau_plateau)):
            for j in range(len(self.tableau_plateau)):
                if self.tableau_plateau[i][j] == "T":
                    couleur = "Orange"
                    affichage = "T"
                elif self.tableau_plateau[i][j]  == "C":
                    couleur = 'Red'
                    affichage = "C"
                elif self.tableau_plateau[i][j] == """~""":
                    couleur = 'Blue'
                    affichage = """~"""
                elif self.tableau_plateau[i][j] == "B":
                    couleur = 'Blue'
                    affichage = """~"""
                b = Button(self.actionLabel,text=affichage,
                           command=lambda i=i, j=j: self.lancement_tir(i, j),
                           width=3,height=3, fg=couleur).grid(row=i,column=j)
        self.actionLabel.update()














