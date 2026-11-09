<p align="center">
  🌐 <b>Select language / Choisir la langue :</b><br>
  <a href="#lang-en"><b>🇬🇧 English</b></a> • <a href="#lang-fr"><b>🇫🇷 Français</b></a>
</p>

---
# 🏰 Dungeon Manager

<a id="lang-en"></a>
# 🇬🇧 English


## Introduction and Project Goal

This project was developed during the **Coding Week** during our cursus at Telecom Nancy. During their second year (Master 1 equivalent), students spend an intensive week dedicated to creating and developing a video game in groups of five.

This group was composed of :
- Lena BESSIERE
- Quentin DELHOMME
- Timothé NINO-LAGADEC
- Anne REGENNASS
- Camilla SCHOESER

The goal was to create a **Dungeon Manager** game using an object-oriented programming language. We chose **Python** along with **Flask** for the web interface.

## Description

**Goofy Dungeon Manager** is an asymetric strategy game, that you can play through the temrinal or a Web interface (Flask). In that game, you are not the hero that tries to reach the treasure : you are the dungeon master. Your mission is to protect your treasure from waves of heroes that progressively become more numerous, smarter, and more determined. Manage your budget, place strategic traps, and deploy monsters to stop the intruders before they reach your loot !

## Installation & Running

### Prerequisites

- Python 3.8+
    
- Dependencies: `Flask`, `Pytest`
    
Install dependencies using:
```bash
pip install flask pytest
```

### Running the Game

- **Web Version (Recommended):**
    
    ```bash
    python3 src/mainWeb.py
    ```
  
Then open your browser and navigate to `http://127.0.0.1:5000`
    
- **Terminal Version:**

    ```bash
    python3 src/mainTerminal.py
    ```

---

## Gameplay & Game Elements

### The Heroes
Each hero has health points (HP) that allow him to survive to some traps, and a specific AI strategy to reach the treasure:
- **BFS (Breadth-First Search):** Finds the mathematically shortest path (though not always the safest regarding traps).
- **Least dangerous :** Evaluates known trap locations and avoids them.
- **Fearless :** Aggressively targets monsters to destroy them. This can act as a distraction, allowing other heroes to reach the treasure unnoticed.

### Defenses
Protect your treasure by placing various elements in your dungeon:
- **Walls :** Block paths physically. Heroes cannot walk through them.
- **Traps :**
    - **Spikes :** Inflict direct damage on heroes. Can be upgraded with money.
    - **Holes :** Heroes fall inside. Be careful! after a certain number of heroes fall in, the hole gets filled and disappears. You can upgrade their size (Small, Medium, Large) to increase capacity.
    - **Runes :** Disorient heroes upon contact. Affected heroes temporarily lose their pathfinding objective and wander off, potentially walking into other traps or monsters.
    - **Fire :** Deals continuous damage over time across several tiles.
- **Monsters :** Hunt down and engage heroes in combat. Monsters also have HP.

#### Upgrades
Certain traps can be upgraded using in-game currency. Upgrading a trap type grants buffs to all future traps of that type. To upgrade, click the "Upgrade" button and confirm your choice in the pop-up menu showing the cost.

### The Budget
You start the game with a limited budget. Every item placed costs money. You can remove placed items, but you will only receive a partial refund—spend wisely! Defeating heroes rewards you with additional funds.

---
## Saves System

As the Dungeon Master, you can save your progress to re-test strategies or resume playing later:

1. **Maps :** Saves only the layout of walls and traps. Useful for replaying specific dungeon setups.

2. **Games :** Saves the complete game state (map layout, score, current budget, wave count, etc.).

Save files are stored as `.json` files in the `/saves` directory and can be loaded at any time from the main menu.

---

## Technical Architecture

The project follows a modular architecture separating game logic from the user interface:

- **`/models` :** Core engine logic:

    - **`gameState.py`:** Manages global game state, scoring, budget, and wave progression.

    - **`dungeon.py`:** Handles grid management, collision detection, and entity placement.

    - **`entity.py`:** Defines core classes (`Hero`, `Monster`, `Trap`).

- **`/strategies` :** AI pathfinding implementations (BFS, modified Dijkstra).

- **`/static` & `/templates`:** Web interface assets (HTML, CSS, JavaScript).

### Web API (Flask)

The frontend communicates with the backend via a JSON API :

- `GET /api/state` : Retrieves the current game state (grid layout, hero positions, budget).
    
- `POST /api/place` : Places an element on the grid.
    
- `POST /api/wave/update` : Computes the next step in the simulation loop.

---
## Testing

This project uses `pytest` to validate damage calculations and AI movement algorithms.
Run the test suite with:

```bash
pytest -v
```

<p align="right">
  <a href="#top">⬆️ <b>Back to top</b></a>
</p>

---

<a id="lang-fr"></a>
# 🇫🇷 Français

## Introduction et Objectifs du projet

Ce projet a été réalisé dans le cadre de la **Coding Week** de Telecom Nancy. En deuxième année (équivalent Master 1), les étudiants ont une semaine de cours banalisée et qui est consacrée à la création d'un jeu en groupe de 5.

Notre groupe ici était composé de :
- Lena BESSIERE
- Quentin DELHOMME
- Timothé NINO-LAGADEC
- Anne REGENNASS
- Camilla SCHOESER

Le but était de concevoir un jeu de `Dungeon Manager` en utilisant un langage orienté objet. Ici, notre choix s'est porté sur **Python**, avec notamment l'usage de la bibliothèque **Flask** pour l'interface Web.

## Description

**Goofy Dungeon Manager** est un jeu de stratégie asymétrique jouable via un terminal ou une interface Web (Flask). 
Dans ce jeu, vous n'êtes pas le héros qui cherche à atteindre le trésor : vous êtes le Maître du Donjon, dont la mission est de protéger votre trésor contre des vagues de héros de plus en plus nombreux, intelligents et déterminés. Pour éviter de perdre votre trésor, utilisez votre intelligence pour gérez votre budget, placez judicieusement vos pièges et envoyez vos monstres pour stopper les intrus.


## Installation & Lancement

### Prérequis

- Python 3.8+
    
- Dépendances : `Flask`, `Pytest`
    
Installez les dépendances nécessaires avec :
```bash
pip install flask pytest
```

### Lancement du jeu

- **Version Web (Recommandé) :**
    
    ```bash
    python3 src/mainWeb.py
    ```
Puis ouvrez votre navigateur à l'adresse `http://127.0.0.1:5000`
    
- **Version Terminal :**

    ```bash
    python3 src/mainTerminal.py
    ``` 
---

## Gameplay & Éléments du jeu

### Les Héros
Chaque héros possède des points de vie (HP) et utilise une stratégie d'IA spécifique pour traverser le donjon :

- **BFS (Breadth-First Search):** Emprunte le chemin le plus court mathématiquement (mais pas toujours le plus sûr face aux pièges).
- **Moins dangereux :** Analyse la position des pièges connus et cherche à les éviter.
- **Fearless (Fearless) :** Traque et attaque les monstres. Cela peut créer une distraction, permettant aux autres héros d'atteindre le trésor pendant ce temps.

### Les Défenses
Pour protéger votre trésor, vous pouvez placer divers éléments dans le donjon :
- **Murs :** Bloquent physiquement le passage. Les héros ne peuvent pas les traverser.
- **Pièges :** 
	- **Piques :** Infligent des dégâts directs aux héros. Améliorables avec de l'argent.
    - **Trous :** Les héros y tombent. Attention : après un certain nombre de héros éliminés, le trou se rebouche et disparaît. Vous pouvez augmenter sa taille (Petit, Moyen, Grand) et donc sa capacité.
    - **Runes :** Désorientent le héros au contact. Celui-ci perd temporairement son objectif et divague, ce qui peut l'amener vers d'autres pièges ou monstres.
    - **Feu :** Inflige des dégâts sur la durée sur plusieurs cases.
- **Monstres :** Traquent et affrontent directement les héros. Ils possèdent également des points de vie.

#### Améliorations
Certains pièges sont améliorables contre de l'argent. L'amélioration d'un type de piège applique des bonus à tous les pièges de ce type posés par la suite. Pour améliorer un piège, cliquez sur le bouton "Upgrade" et validez votre choix sur la fenêtre d'information.

### Budget
Vous disposez d'un budget initial. Chaque élément posé a un coût. La suppression d'un élément ne vous rembourse qu'une partie de son prix d'achat : réfléchissez bien avant de construire ! Éliminer des héros vous rapporte de l'argent supplémentaire.

---
## Sauvegardes

En tant que Maître du Donjon, vous pouvez sauvegarder votre progression pour rejouer ou tester différentes stratégies :

1. **Maps :** Enregistre uniquement la disposition des murs et pièges. Pratique pour rejouer sur une carte spécifique.
    
2. **Parties :** Enregistre l'état complet du jeu (carte, score, budget, numéro de la vague, etc.).

Les fichiers de sauvegarde sont stockés au format `.json` dans le dossier `/saves` et peuvent être chargés à tout moment depuis le menu principal.

---

## Architecture Technique

Le projet suit une structure modulaire séparant la logique de jeu de l'interface utilisateur :

- **`/models`** : Cœur du moteur de jeu :
    
    - `gameState.py` : Gère l'état global, le score, le budget et le cycle des vagues.
        
    - `dungeon.py` : Gère la grille, les collisions et le placement des objets.
        
    - `entity.py` : Définit les classes `Hero`, `Monster` et `Trap`.
        
- **`/strategies`** : Implémentations des algorithmes de déplacement des IA (BFS, Dijkstra modifié).
    
- **`/static` & `/templates`** : Fichiers Web (HTML/JS/CSS).
    

### API Web (Flask)

Le frontend communique avec le backend via une API JSON :

- `GET /api/state` : Récupère l'état actuel (grille, héros, budget).
    
- `POST /api/place` : Place un élément sur la grille.
    
- `POST /api/wave/update` : Calcule le prochain tour de la simulation. 

---
## Tests

Le projet utilise `pytest` pour garantir la stabilité des calculs de dégâts et des déplacements d'IA.

Lancez la suite de tests avec :
```bash
pytest -v
```

---

## Rendu final

<video src="CodingWeek_Demo.mp4" controls width="100%">
  Votre navigateur ne supporte pas la lecture de vidéos.
</video>

<p align="right">
  <a href="#top">⬆️ <b>Retour en haut</b></a>
</p> 