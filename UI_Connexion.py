from tkinter import *
from tkinter import messagebox


def fenetre_connexion():

    def authentification():
        fenetre.quit()
        fenetre.destroy()

    def afficher_erreur(erreur):
        fenetre.withdraw()
        messagebox.showerror(title="Error", message=erreur)

    def afficher_message(message):
        fenetre.withdraw()
        messagebox.showinfo(title="Information", message=message)

    fenetre = Tk()

    fenetre.wm_title("Connexion")

    # Labels

    title_label = Label(fenetre, text="Bienvenue dans la bataille navalle")
    title_label.grid(row=1, column=3)

    login_label = Label(fenetre, text="Login")
    login_label.grid(row=2, column=3)

    password_label = Label(fenetre, text="Password")
    password_label.grid(row=3, column=3)

    # Entries
    login_text = StringVar()
    login_entry = Entry(fenetre, textvariable=login_text)
    login_entry.grid(row=2, column=4)

    password_text = StringVar()
    password_entry = Entry(fenetre, textvariable=password_text)
    password_entry.grid(row=3, column=4)
    password_entry.config(show="*")

    # Button
    connexion_button = Button(fenetre, text="Connexion", width=12, command=authentification)
    connexion_button.grid(row=5, column=4)

    fenetre.mainloop()
    return login_text.get(), password_text.get()
