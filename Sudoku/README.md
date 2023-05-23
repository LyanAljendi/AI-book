# Sudoku

Vous trouverez ci-dessous les instructions et détails sur le jeu du sudoku.
Le but du jeu étant de remplir la grille du sudoku avec les chiffres 1 à 9
chacun présent une et une seule fois dans chaque ligne, colonne et bloc.

Le jeu est présenté avec deux AI différentes, l'une avec une recherche classique
et l'autre avec un algorithme génétique.


## Installation

Pour installer l'application, commencez par copier le dépot du livre ([AI-book sur github][ia-gh]),
soit en recupérant l'archive zip depuis github, soit à l'aide de l'outil git:
```
git clone https://github.com/iridia-ulb/AI-book
```

Puis, accedez au dossier:

```bash
cd Sudoku
```

Après avoir installé python et poetry, rendez vous dans ce dossier et installez les
dépendances du projet:

```bash
poetry install
```

## Utilisation

Vous pouvez ensuite lancer le jeu dans l'environnement virtuel nouvellement créé.
Le jeu en mode recherche se lance comme ceci:
```bash
poetry run python main.py -f sudokus/sudoku1.txt -a optimized_search -hf smallest_dof
```
Une fois lancé, vous pouvez jouer vous même avec la grille en entrant les chiffres
en utilisant à votre clavier et votre souris; ou alors *lancer l'IA* en appuyant sur 
la *barre espace*.

### Sélection de la grille de Sudoku
Dans cette ligne de commande, l'option `-f`, represente l'instance du sudoku à résoudre,
par defaut, on utilise une instance contenue dans le  fichier `sudokus/sudoku1.txt`.
Vous trouverez d'autres instances à tester dans le fichier `sudokus/sudokus.txt`.

Les fichiers doivent être formatés tels que la grille du sudoku à remplir est constituée
d'une serie de chiffre sur une ligne, en lisant la grille de gauche à droite et de haut
en bas, et en remplaçant les espaces libres par des 0.

Voici un exemple de contenu de fichier sudoku :
```
200307801000200070000609030070005620900000507600000009001000000000002980000708002
```

### Sélection de l'algorithme de résolution
Pour selectionner l'algorithme à utiliser dans le jeu, changez l'option `-a` dans la ligne de commande.
Cette option peut prendre 3 valeurs, `genetic` pour l'algorithme génétique, `visual_search` pour l'algorithme de recherche
dont l'exécution est visualisée, ou `optimized_search` pour l'algorithme de recherche optimisé, s'exécutant en un temps minimal.
Pour ce dernier, un argument supplémentaire est obligatoire : `-hf`.

### Sélection de la fonction heuristique
La fonction heuristique utilisée par l'algorithme de recherche amélioré doit être spécifiée via la commmande
`-hf`. Cet argument peut prendre la valeur `smallest_dof`, correspondant à une fonction privilégiant les
cellules ayant peu de différentes valeurs possibles, et la valeur `smallest_dof_and_local_impact`, privilégiant
les cellules ayant peu de différentes valeurs possibles **et** étant impactées par la dernière cellule remplie.

### En résumé:
```
usage: main.py [-h] [-f FILE] [-a {genetic, visual_search, optimized_search}] [-hf {smallest_dof, smallest_dof_and_local_impact}]

Launch the sudoku game

optional arguments:
  -h, --help            show this help message and exit
  -a {search,genetic}, --algorithm {search,genetic}
                        Choose the algorithm to execute
  -f FILE, --file FILE  Sudoku instance to solve
  -hf {smallest_dof, smallest_dof_and_local_impact}, --heuristic {smallest_dof,smallest_dof_and_local_impact}
                        Choose the heuristic function of optimized_search
```

[ia-gh]: https://github.com/iridia-ulb/AI-book



