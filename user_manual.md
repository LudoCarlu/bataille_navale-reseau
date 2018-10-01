# User manual
CARLU Ludovic - FAIVRE Maxime - LE BORGE Kévin

## Introduction - Prérequis
On considère que le serveur de jeu et les différents clients sont sur des machines UNIX. Cela implique donc que python soit pré-installé. 

Il faut également installer des dépendances pour que l'application fonctionne correctement : pandas et tkinter.

Pandas nous permet de lire le fichier des users et dépend aussi de Numpy.

`pip3 install pandas`

Tkinter nous est utile pour la partie graphique.

`pip3 install tkinter`

Lors du lancement des instances du jeu il faut être vigilant et lancer avec `python3` (le code a été produit avec la version 3.6 de Python)

## Initialisation du jeu
Dans un premier temps, il faut récupérer les sources et extraire dans un dossier.

Il faut ensuite se positionner dans ce dossier pour pouvoir lancer l'instance sur le serveur

`python3 battleship-server.py`


Il faut maintenant lancer le premier client admin

`python3 client.py` 

Sur ce client on se connecte en admin avec les crédentials contenus dans le fichier : *users.csv*
Soit :
    
    login : admin
    password : admin


A partir de ce moment, l'administrateur peut choisir la taille de la grille pour la bataille navale.
Dès lors qu'il a choisit la taille de la grille, les différents joueurs peuvent se connecter grâce au lancement de plusieurs interfaces client.

`python3 client.py` 

Les différents login des clients se trouvent aussi dans le fichier *users.csv*

Une fois les différents joueurs connectés, l'administrateur doit placer ces bateaux. 

1. Il sélectionne une case en cliquant dessus, cela positionne la tête du bateau
2. Il sélectionne une orientation (horizontal/vertical)
3. Puis une taille (petit, moyen ou grand)

Nous avons fixé le nombre maximum de bateau à 3.

Dès lors que l'administrateur à placer tous ces bateaux, une interface graphique apparait pour proposer à l'administrateur d'accepter les différents joueurs sur sa partie.


## Jeu

La partie commence et le serveur invite le premier joueur à lancer un tir.

Les joueurs lance un tir à tour de rôle et le serveur leur renvoie l'état de leur tir et le nouveau plateau de jeux.

L'affichage se décompose en 3 caractères :

- "~" représente une case vide ou tir manqué.
- "T" représente une case touchée
- "C" représente un bateau coulé

Une casé touché est égale à 1 point et un bateau coulé à 3 points.

Le jeu se termine lorsque que tous les bateaux ont été coulés.