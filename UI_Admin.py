from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *

def fenetre_choix_dimensions(titre="Choix de la taille du tableau et placement"):

    toplevel = Tk()
    global choix

    choix=10
    toplevel.attributes("-topmost", True)
    stock_type_of_id = (10, 15, 20)
    list_taille = Listbox(toplevel,selectmode='unique',height=3)
    list_taille.pack()
    for elt in stock_type_of_id:
        list_taille.insert(END,elt)



    def OK_list():
        global choix
        choix = list_taille.curselection()[0]
        toplevel.quit()
        toplevel.destroy()

    Button(toplevel, text='OK', padx=100, pady=10, command=OK_list).pack(side=RIGHT)
    toplevel.mainloop()
    return stock_type_of_id[choix]


def fenetre_placement(tailleplateau,titre="Placement des bateaux"):

    toplevel = Tk()
    global taille,pos,pos_y,pos_x
    taille=""
    pos = ""
    pos_x = 0
    pos_y = 0
    toplevel.attributes("-topmost", True)
    stock_type_of_id = ("petit", "moyen", "grand")
    list_taille = Listbox(toplevel, selectmode='unique', height=3,exportselection=False)
    list_taille.grid(row=tailleplateau+1)
    for elt in stock_type_of_id:
        list_taille.insert(END, elt)

    stock_pos = ("horizontale", "verticale")
    list_pos = Listbox(toplevel, selectmode='unique', height=2,exportselection=False)
    list_pos.grid(row=tailleplateau+2)
    for elt in stock_pos:
        list_pos.insert(END, elt)

    label_x = Label(toplevel,text=" position x : "+str(pos_x))
    label_x.grid(row=0,column=0)
    label_y = Label(toplevel, text=" position x : " + str(pos_y))
    label_y.grid(row=1, column=0)

    def definition_pos(x,y):
        global pos_x, pos_y
        pos_x = x
        pos_y = y
        label_x.config(text=" position x : "+str(pos_x))
        label_y.config(text=" position x : "+str(pos_y))

    frame_grille = LabelFrame(toplevel, text="Grille").grid(row=0)
    for i in range(tailleplateau):
        for j in range(tailleplateau):
            b = Button(frame_grille,text='-',
                       command=lambda i=i, j=j: definition_pos(i, j),
                       width=3,height=3, fg="Blue").grid(row=i, column=j+1)
    def OK_list():
        try:
            global taille,pos
            taille = list_taille.curselection()[0]
            pos = list_pos.curselection()[0]
            toplevel.quit()
            toplevel.destroy()
        except:
            showerror("Erreur","Veuillez sélectionner tous les champ")

    Button(toplevel, text='OK', padx=100, pady=10, command=OK_list).grid(row=tailleplateau+3)
    toplevel.mainloop()
    return stock_type_of_id[taille], \
           stock_pos[pos],\
           pos_x,pos_y
