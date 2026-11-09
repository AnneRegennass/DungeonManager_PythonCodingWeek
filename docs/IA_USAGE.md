# Usage de l'IA
### Interface WEB
Utilisation de l'IA pour générer le script Javascript faisant le lien avec le background
#### Modèle : Gemini 3 Pro

**Renseigné :** Le document de background, le templates actuel html et les models

**Prompt :** Salut Gemini, on développe un dungeon maker en Python3 dans le cadre d'un projet informatique. Nous avons fini le fonctionnement interne du jeu, tu peux trouver le fonctionnement dans les fichiers Python. Peux-tu modifier le template afin de créer les scripts de communication entre le backend et le frontend ?

**Données récupérées :** Dans index.html : la fonction refresh, setMode, les prototypes de place, startWave, updateWave. Des modifications on dû être apporté/modifé.
Dans mainWeb.py : la fonction placeElement. On a dû repasser derrière pour que la fonction "effacer" marche correctement.


**Renseigné :** Le document template de la page principale

**Prompt :** Okay, maintentant tu es un développeur front-end depuis 20 ans. De plus, tu as une grande expérience dans le design graphique de jeu vidéo, et ta spécialité est justement les jeux médiévaux en pixel art. Essaie de créer un environnement style auberge médiévale, avec un donjon pour le terrain depuis cette template

**Données récupérées :** Le nouveau code css de la page. Il y a eu quelques arrangements à faire car il y avait parfois trop de div et le rendu visuel était donc incohérent avec la charte graphique (trop de cadre dans des cadres dans des cadres...)

**Renseigné :** Le backend de la page d'acceuil

**Prompt :** Super ! Maintenant, peux-tu me créer une page d'accueil dans laquelle on peut également choisir la taille de la grille ? Fait le en accord avec le backend s'il te plait

**Données récupéré :** Le template welcome.html et un add-on du css


**Prompt :** Peux-tu me montrer ce que tu pourrais faire comme page de Game Over ? Déploie tes talents et ton inventivité !

**Données récupérés :** La partie Game Over de index.html et le css. Modifications apporté car la fonction de game over ne se liait pas bien aux autres

-------------

**Suite :** "Veux-tu que je t'aide à améliorer le design (CSS) pour que ça ressemble moins à un tableur et plus à un jeu ?"

**Réponse :** "je veux bien que tu m'aides pour le css "

**Données récupérées :** La majorité du fichier CSS

### Tests unitaires
Utilisation de l'IA pour mettre en place des tests unitaires et avoir quelques exemples
#### Modèle : GPT-4.1-mini

**Renseigné :** La structure du projet, le fichier dungeon.py

**Prompt :** Comment faire des fichiers de tests unitaires ? 

**Données récupérées :** Explications pour installer pytest et exécuter les tests unitaires, fichier pytest.ini, un début du fichier test_dungeon.py avec 5 tests unitaires

-------------

### Tests unitaires strategies

**Contexte :** Création et débogage des tests unitaires pour les stratégies de déplacement (test_strategies.py).

**Prompt :** "tu peux m'aider à faire des tests unitaires pour cette nouvelle startegie stp?" 

**Décisions et actions :**
- Implémentation d'un MockGame : Création d'une classe légère pour simuler l'état du jeu (GameState). Cela permet de tester les stratégies complexes comme Fearless sans initialiser tout le moteur de jeu.

- Ajout de la méthode is_monster_on(pos) dans le Mock pour répondre aux appels internes de l'algorithme.
- Correction de la logique Fearless :

    - Bords du donjon : Ajout de vérifications strictes pour éviter que l'IA ne tente d'aller dans des coordonnées négatives 

    - Ciblage : Modification de la reconstruction du chemin pour qu'elle vise le monstre trouvé par Dijkstra et non la position par défaut du trésor, évitant ainsi des KeyError.
    
-  Tests :

    - test_bfs : Vérifie le chemin le plus court et le contournement des murs.

    - test_less_dangerous : Valide que l'IA préfère un détour plutôt que de marcher sur un piège Spike à haut niveau.

    - test_fearless : Confirme que le héros priorise le monstre le plus proche avant de se diriger vers le trésor.

**Remarques techniques :**
L'utilisation de pytest est recommandée pour lancer ces tests automatiquement via la commande pytest tests/test_strategies.py.

--------------

### Débogger les échecs des tests unitaires

**Contexte :** identifier et corriger plus rapidement les problèmes détectés par les tests unitaires

**Renseigné :** message d'erreur affiché dans le terminal lors de l'exécution des tests

**Prompt :** "comment résoudre ce probleme ?"

**Réponse IA :** analyse du message d’erreur et propositions de pistes de correction adaptées

**Décision :** application des indications fournies par l’IA pour corriger le problème détecté par les tests

-------------

### Système de gestion des sauvegardes 

**Contexte :** Séparation des fichiers de sauvegarde entre "Layouts de Map" et "Sessions de Jeu" avec calcul de coût théorique. 

**Prompt :** "Je veux sauvegarder les maps et les parties sur deux zones séparées (saves/maps et saves/games). Comment vérifier que les dimensions de la map correspondent avant de la charger pour éviter les erreurs d'affichage ?"

**Réponse IA :** Mise à jour des routes Flask et modification de gameState.py pour lever des ValueError personnalisées. 

**Décision :**
- Gardé : La structure des dossiers os.path.join et la logique de validation côté serveur.
- Modifié : Ajout de pop-ups alert() dans index.html pour traduire les erreurs techniques en messages clairs pour l'utilisateur. 

**Remarques :** Approche rigoureuse pour garantir l'intégrité des données : le jeu refuse désormais de charger un fichier corrompu ou de taille incompatible

--------------

### Sérialisation et restauration des objets complexes (Pièges et Monstres)

**Contexte :** Problème de perte de données lors du chargement : les types de pièges (Feu, Rune) étaient convertis en pieges simples. 

**Prompt :** "Mes pièges sont enregistrés comme des pièges simples, mais j'ai des classes spécifiques (Spike, Fire, Rune). Comment sauvegarder la classe et le niveau pour les recréer fidèlement ?" 

**Réponse IA :** Utilisation de __class__.__name__ dans la méthode to_dict et d'un mapping de classes dans from_dict.

**Décision :**
- Gardé : Le stockage sous forme de dictionnaire {"class": ..., "level": ...}.
- Modifié : Correction d'une erreur d'indentation critique dans la boucle de restauration des monstres qui causait une UnboundLocalError. 

**Remarques :** Cette interaction a permis de passer d'une sauvegarde de "symboles" à une sauvegarde de "véritables objets Python" possédant leurs propres attributs de dégâts et PV.


--------------

### Extension du système de persistance au mode Terminal

**Contexte :** Alignement des fonctionnalités de l'interface Terminal avec l'interface Web pour garantir la portabilité des données.

**Prompt :** "Je dois implémenter les sauvegardes et les chargements dans le mode terminal. Je veux utiliser la même logique que pour la version Web, en séparant les dossiers maps et games, tout en gérant les erreurs de budget et de dimensions."

**Réponse IA :** L'IA a proposé de créer deux fonctions utilitaires (handle_save_console et handle_load_console). Elle a suggéré d'utiliser os.listdir pour lister dynamiquement les fichiers JSON disponibles dans saves/maps et saves/games, offrant ainsi un menu de sélection numéroté à l'utilisateur. La réponse incluait l'intégration de blocs try/except pour capturer les ValueError levées par le GameState lors de la validation du budget ou de la taille du donjon.

**Décision :**
- Gardé : L'arborescence de fichiers partagée, permettant de commencer une partie sur le Web et de la reprendre en Terminal (ou inversement).
- Appliqué : La réutilisation directe de la méthode load_from_file du GameState, garantissant que toutes les règles métier (coût théorique, vérification des dimensions) sont appliquées uniformément.

**Remarques :** L'implémentation console bénéficie désormais de la même robustesse que la version Web : le programme ne crash plus si l'utilisateur tente de charger une map trop grande, grâce à la gestion d'exception proposée.

--------------

### Syntaxe diagramme de séquence

**Contexte :** Apprendre la syntaxe .puml pour faire le diagramme de séquence demandé.

**Prompt :** Comment faire un diagramme de séquence en .puml

**Réponse IA :** L'IA a expliqué en 9 points comment faire un diagramme de séquence dans un fichier .puml (structure de base d'un diagramme de séquence, déclarer les participants, messages entre participants, activation(barre de vie), conditions, boucles, messages asynchrones, exemple complet, générer le diagramme).

**Décision :** 
- Gardé : la syntaxte générale du fichier, et l'utilisation des boucles.

--------------

### Afficher la bordure externe de la grille (murs)

**Contexte :** Définir la bordure externe de la grille avec des murs (sur lesquels le joueur ne peut pas poser d'élément, et que le héros ne peut pas parcourir)

**Renseigné :** La méthode api/state dans mainWeb.py

**Prompt :** "Comment afficher une bordure autours de ma grille ?"

**Réponse IA :** Un extrait de code pour ajouter des murs sur les cases de la grilles qui sont le bord

**Décision :**
- Reprendre le code proposé par l'IA (principalement la logique) et l'adapter pour afficher la bordure
- Gérer les indices pour éviter un décalage d'une case vers le haut et vers la gauche des éléments de la grille (héros, pièges, etc)

--------------

### Correction bug ajout de pièges sur la grille

**Contexte :** Quand on ajoute plusieurs fois le même élément sur la même case sur la grille, de l'argent est débité, alors que ce serait mieux que le solde reste constant.

**Renseigné :** Méthode BuyElement dans gameState.py

**Prompt :** "quand je pose plusieurs fois le meme piege sur la meme case, ca me débite de largent, alors que ca ne devrait pas. Tu peux m'aider à corriger ça ? "

**Réponse IA :** Script qui traite les cas particuliers où on veut ajouter le même élément sur une case 

**Décision :** Ajouter cet extrait de code à la méthode BuyElement

--------------

### Afficher une barre qui indique le niveau de vie sur les héros

**Contexte :** Afficher une barre au dessus de chaque héros qui indique son niveau de vie (hp) pendant la partie

**Renseigné :** la classe startWave dans gameState

**Prompt :** "afficher le niveau de vie des héros quand on clique dessus sous forme de barre de progression"

**Réponse IA :** du code javascript pour calculer la longueur de la barre de progression et l'afficher (CSS)

**Décision :** reprendre ce code, le corriger pour prendre la bonne valeur de hpmax, et réadapter ce code pour afficher le niveau de vie des monstres

--------------

### Rédiger le gitignore

**Contexte :** Eviter de push toutes les dépendances du projet à chaque fois

**Prompt :** comment ignorer le venv dans mon git quand je commit et push ?

**Réponse IA :** lignes à ajouter dans le fichier gitignore

--------------