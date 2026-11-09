# ROADMAP – Projet Dungeon Manager

## 1. Vision du projet
- Objectif général :

- Public cible / utilisateur :

- Résultat attendu en fin de semaine :

## 2. Conventions

- *#Statuts des tâches*# :
- `TODO` : à faire
- `DOING` : en cours
- `DONE` : terminé
- *#Sprints*# :
- `DAY_1` à `DAY_5` (1 sprint par jour)
- Les détails de chaque sprint sont dans :
`SPRINT_PLANNING_DAY_X.md` et `SPRINT_RETROSPECTIVE_DAY_X.md`.

## 3. Backlog global

> Liste des fonctionnalités et tâches importantes, avec une cible de sprint.

| ID | User story / tâche | Sprint cible | Priorité | Etat |
|---|---|---|----|----|
| US1 | En tant que Joueur, je dois pouvoir afficher une grille de 32x32 cases sur une page web | DAY_1 | Haute | DONE |
| US2 | En tant que Joueur, je dois pouvoir afficher une grille de 32x32 cases sur un terminal | DAY_1 | Haute | DONE |
| US3 | En tant que Joueur, je dois pouvoir poser des murs et des pièges dans mon donjon | DAY_1 | Haute | DONE |
| US4 | En tant que Joueur, je dois pouvoir poser des monstres dans mon donjon | DAY_3 | Faible | DONE |
| US5 | En tant que Joueur, je dois pouvoir lancer une vague de héros dans mon donjon | DAY_1 | Haute | DONE |
| US6 | En tant que Joueur, je dois pouvoir choisir la difficulté de la vague de héros | DAY_2 | Haute | DONE |
| US7 | Implémenter la stratégie d'IA de "plus court chemin" | DAY_1 | Haute | DONE |
| US8 | Implémenter une seconde stratégie d'IA "le chemin le moins dangereux" | DAY_2 | Haute | DONE |
| US9 | En tant que Joueur, je dois pouvoir avoir accès à mon argent et acheter/vendre des éléments | DAY_2 | Haute | DONE |
| US10| Implémenter différents types de pièges (piège permanent, à usage unique, trou qui se rempli) | DAY_2 | Faible | DONE | 
| US11| Le nombre de héro par vague augmente au fur et à mesure | DAY_3 | Faible | DONE | 
| US12| En tant que Joueur, je dois pouvoir voir le nombre de héro dans la prochaine vague | DAY_3 | Faible | DONE | 
| US13| Implémenter le calcul du score | DAY_2 | Haute | DONE | 
| US14| S'assurer qu'il existe toujours un chemin possible pour arriver au trésor | DAY_1 | Haute | DONE | 
| US15| Implémenter différents types de héros | DAY_4 | Faible | DONE | 
| US16| En tant que Joueur, je dois pouvoir améliorer mes pièges | DAY_4 | Faible | DONE | 
| US17| L'état du donjon est conservé ou non d'une vague à une autre | DAY_3 | Faible | DONE | 
| US18| Sauvegarder/charger un donjon | DAY_1 | Haute | DONE | 
| US19| Implémenter l'affichage du récapitulatif en fin de vague | DAY_3 | Moyenne | DONE | 
| US20| Ajouter des évenements aléatoires | DAY_4 | Faible | DONE | 
| US21| Ajouter des messages d'ambiance | DAY_4 | Faible | TODO | 
| US22| Implémenter une troisième stratégie d'IA | DAY_4 | Faible | DONE | 
| US23| Mise en place de tests unitaires | En continu | Haute | DONE | 
| US24| Faire diagramme de classe associé | En continu | Haute | DONE | 
| US25| Faire un ou 2 diagramme de séquences | DAY_5 | Haute | DONE | 
| US26| Préparer la vidéo de démonstration | DAY_5 | Haute | DOING | 
| US27| Finaliser le code et nettoyage | DAY_5 | Haute | DONE | 
| US28| Ajouter une documentation détaillée chaque jour | En continu | Haute | DONE | 
| US29| En tant que Joueur, je dois pouvoir voir les points de vie des héros | DAY_3 | Faible | DONE |
| US30| En tant que Joueur, je dois pouvoir voir les points de vie restant de mes pièges et/ou de mes monstres| DAY_3 | Faible | DONE |
| US31| Ajouter graphismes plus détaillés à la version web | DAY_4 | Faible | DONE |

## 4. Vue par sprint (résumé)

### Sprint DAY_1 – [5/01/26]
- *#Objectif du jour*# : Avoir un jeu de base qui fonctionne, au moins sur le terminal.

- *#User stories ciblées*# : US1, US2, US3, US5, US7, US14.

### Sprint DAY_2 – [6/01/26]
- *#Objectif du jour*# : Compléter la version terminal de la veille et la débuguer (ajouter un autre niveau de difficulté, régler les problèmes liés aux achats/ventes), documenter les fonctions créées, commencer l'interface web et au mieux, avoir le jeu fonctionnel sur web.

- *#User stories ciblées*# : US6,US8, US9, US13, US1, US24, US28, US10

### Sprint DAY_3 – [7/01/26]
- *#Objectif du jour*# : Nettoyer le code et corriger les bugs la veille, continuer la doc, ajouter des monstres, ajouter la gestion des différents héros par vagues (pas être sur une même case, départ des héros en différés, ...), commencer DA, et implémenter des tests unitaires

- *#User stories ciblées*# : US4, US10, US11, US12, US18, US23, US24, US28

### Sprint DAY_4 – [8/01/26]
- *#Objectif du jour*# : Stabiliser le projet en corrigeant les problèmes de Git et en nettoyant le code. Finaliser les mécaniques de jeu importantes (pièges, vagues, IA, récap de fin de vague, système de sauvegarde) et améliorer la lisibilité pour le joueur (PV, coûts, graphismes). Mettre à jour la documentation et le diagramme de classes.

- *#User stories ciblées*# : US12, US15, US16, US18, US19, US22, US23,US24,US27,US28,US30,US31


### Sprint DAY_5 – [9/01/26]
- *#Objectif du jour*# : Finaliser l’expérience de jeu : équilibrer la difficulté et l’économie, gérer la fin de partie et améliorer les retours visuels (récapitulatifs, messages d'ambiance). Finaliser le projet : compléter les documents (diagramme de classe, diagramme de séquence, ), compléter les tests unitaires, finaliser et nettoyer le code, préparer la vidéo de démonstration

- *#User stories ciblées*# : US20, US21, US23, US24, US25, US26, US27, US28, US29, US30, US31

## 5. Améliorations futures 
- Ajouter des messages d'ambiance