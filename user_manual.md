#User manual
CARLU Ludovic - FAIVRE Maxime - LE BORGE Kévin

##Introduction - Prérequis
On considère que le serveur de jeu et les différents clients sont sur des machines UNIX. Cela implique donc que python est pré-installé. 

Il faut également installer des dépendances pour que l'application fonctionne correctement : pandas et tekinter.

Pandas nous permet de lire le fichier des users et dépend aussi de Numpy.

`pip3 install pandas`

Tekinter nous est utile pour la partie graphique.

`pip3 install tekinter`

Lors du lancement des instances du jeu il faut être vigilant et lancer avec `python3` et non python.

##Initialisation du jeu
Dans un premier temps, il faut récupérer les sources et extraire dans un dossier.

Il faut ensuite se positionner dans ce dossier pour pouvoir lancer l'instance sur le serveur

`python3 battlehip-server.py`


Il faut maintenant lancer le premier client admin

`python3 client.py` 

Sur ce client on se connecte en admin avec les crédentials contenus dans le fichier *users.csv*

A partir de ce moment, les différents joueurs peuvent lancer le jeu et se connecter

`python3 client.py` 

Une fois les différents joueurs connectés, il est possible de commencer la partie.

Lors du lancement de la partie, il faut choisir la taille de la table de jeu.

##Jeu

