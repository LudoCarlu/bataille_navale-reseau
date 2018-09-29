from tkinter import *


class UI_Client (Frame):
    def __init__(self, fenetre, initialPlateau, **kwargs):
        LabelFrame.__init__(self, fenetre, text="Interface client",
                            borderwidth=6, **kwargs)
        self.score=0
        self.pseudo ="Test"
        self.initialPlateau=initialPlateau

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

        for i in range(len(self.tableau_plateau)):
            for j in range(len(self.tableau_plateau)):
                b = Button(self.actionLabel,text=self.tableau_plateau[i][j],
                           command=lambda i=i, j=j: self.lancement_tir(i, j),
                           width=3,height=3, fg="Blue").grid(row=i,column=j)


    def traitementstringPlateau(self):
        mon_plateau = self.initialPlateau[:-1].split("\n")
        for i in range(len(mon_plateau)):
            mon_plateau[i] = mon_plateau[i].split(" ")
        return mon_plateau

    def lancement_tir(self, row, col):
        print("Lancement du tir")
        print(row,col)

        ## fonction du client/serveur
        self.etat_du_tir = "touche"
        nouveau_plateau ="~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ T ~ ~ ~\n~ ~ ~ ~ C C C ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n"
        self.score=1
        ##

        self.initialPlateau = nouveau_plateau
        self.tableau_plateau = self.traitementstringPlateau()

        self.actualiser_plateau(row,col)
        self.textMessages.configure(state='normal')
        self.textMessages.insert(END,self.etat_du_tir+"\n")
        self.textMessages.configure(state='disabled')

        self.labelScore.config(text="Score : "+str(self.score))

    def actualiser_plateau(self,row,col):
        print(self.tableau_plateau[row][col])
        for i in range(len(self.tableau_plateau)):
            for j in range(len(self.tableau_plateau)):
                if self.tableau_plateau[i][j] == "T":
                    couleur = "Orange"
                elif self.tableau_plateau[i][j]  == "C":
                    couleur = 'Red'
                elif self.tableau_plateau[i][j] == """~""":
                    couleur = 'Blue'
                b = Button(self.actionLabel,text=self.tableau_plateau[i][j],
                           command=lambda i=i, j=j: self.lancement_tir(i, j),
                           width=3,height=3, fg=couleur).grid(row=i,column=j)









sizePlateau = 10
fenetre = Tk()
plateau = "~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n~ ~ ~ ~ ~ ~ ~ ~\n"
fenetre.title("Interface Client")
UI_Client(fenetre,plateau)
fenetre.mainloop()




