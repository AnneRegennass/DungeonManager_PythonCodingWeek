from models.dungeon import Dungeon
from models.entity import *
from models.gameState import GameState
import os

# Chemins cohérents avec la version Web
SAVE_DIR = "saves"
MAPS_DIR = os.path.join(SAVE_DIR, "maps")
GAMES_DIR = os.path.join(SAVE_DIR, "games")

def handle_save_console(game):
    '''
    :entrée: GameState game
    :sortie: void
    :description: Affiche le menu Sauvegarde dans le terminal et gère l'enregistrement de la partie game.
    '''
    print("\n=== MENU SAUVEGARDE ===")
    print("[1] Sauvegarder la Map ")
    print("[2] Sauvegarder la Partie ")
    choix = input("Votre choix : ")
    
    name = input("Nom du fichier : ")
    
    if choix == "1":
        filename = os.path.join(MAPS_DIR, f"{name}.json")
        game.saveMap_to_file(filename) # Utilise la méthode existante
        print(f" Map enregistrée dans {filename}")
    elif choix == "2":
        filename = os.path.join(GAMES_DIR, f"{name}.json")
        game.saveGame_to_file(filename) # Utilise la méthode existante
        print(f" Partie enregistrée dans {filename}")

def handle_load_console(game):
    '''
    :entrée: GameState game
    :sortie: void
    :descrption: Affiche et gère le menu de chargement de carte.
    '''
    print("\n=== MENU CHARGEMENT ===")
    print("[1] Charger une Map ")
    print("[2] Charger une Partie ")
    choix = input("Votre choix : ")
    
    target_dir = MAPS_DIR if choix == "1" else GAMES_DIR
    
    # Lister les fichiers disponibles
    files = [f for f in os.listdir(target_dir) if f.endswith('.json')]
    if not files:
        print("Aucun fichier trouvé.")
        return

    print("\nFichiers disponibles :")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    
    try:
        idx = int(input("Sélectionnez le numéro : ")) - 1
        full_path = os.path.join(target_dir, files[idx])
        
        # Le GameState gère déjà les erreurs de budget et de dimensions
        if game.load_from_file(full_path):
            print(f" Chargement réussi depuis {files[idx]}")
    except ValueError as e:
        print(f" Erreur : {e}")
    except Exception as e:
        print(f"Erreur imprévue : {e}")



def entity_to_chr(entity_type, entity):
    '''
    :entrée: EntityType entity_type, entity
    :sortie: chr
    :description: Renvoie le charactère permettant d'afficher dans le terminal l'élément entity, de type entity_type.
    '''
    if entity_type == EntityType.EMPTY:
        return "."
    elif entity_type == EntityType.WALL:
        return "#"
    elif entity_type == EntityType.ENTRY:
        return "E"
    elif entity_type == EntityType.TREASURE:
        return "T"
    elif entity_type == EntityType.TRAP:
        if isinstance(entity, Hole) and entity.level == 1 :
            return "°"
        elif isinstance(entity, Hole) and entity.level == 2:
            print("moyen")
            return "o"
        elif isinstance(entity, Hole) and entity.level == 3:
            print("grand")
            return "O"
        elif isinstance(entity, Rune):
            return "@"
        elif isinstance(entity, Fire):
            return "F"
        else :
            return "^"
    elif entity_type == EntityType.HERO:
        return "H"
    elif entity_type == EntityType.MONSTER:
        return "M"



def display_dungeon(game_state):
    '''
    :entrée: GameState game_state
    :sortie: void
    :description: Affiche le donjon de game dans le terminal.
    '''

    display_grid = [['.' for _ in range(game_state.dungeon.width)] for _ in range(game_state.dungeon.height)]

    for x in range(game_state.dungeon.width):
        for y in range(game_state.dungeon.height):
            entity_type = game_state.dungeon.get_cell(x, y)
            if entity_type == EntityType.TRAP:

                if isinstance(game_state.dungeon.trap[(x,y)], Hole) :
                    display_grid[y][x] = entity_to_chr(entity_type, game_state.dungeon.trap[(x,y)])
                elif isinstance(game_state.dungeon.trap[(x,y)], Fire) :
                    display_grid[y][x] = entity_to_chr(entity_type, game_state.dungeon.trap[(x,y)])
                elif isinstance(game_state.dungeon.trap[(x,y)], Rune) :
                    display_grid[y][x] = entity_to_chr(entity_type, game_state.dungeon.trap[(x,y)])
                else:
                    display_grid[y][x] = entity_to_chr(entity_type, None)

            else :
                display_grid[y][x] = entity_to_chr(entity_type, None)

    loaded_heroes = game_state.get_loaded_heros()
    for hero in loaded_heroes:
        display_grid[hero.pos[1]][hero.pos[0]] = 'H'
    

    for x in range(game_state.dungeon.width):
        for y in range(game_state.dungeon.height):
            
            print(display_grid[x][y], end=" ")
            
        print()


def main():
    '''
    :entrée: void
    :sortie: void
    :description: Fonction main, jeu dans le terminal.
    '''
    os.system('cls' if os.name == 'nt' else 'clear') 

    dungeon = Dungeon(width=10, height=10)
    game = GameState(dungeon)
    
    while True:

        print("\n=== DUNGEON MANAGER ===")
        print(f" Vague en cours : {game.nbWave}   |   Budget : {game.budget} or   |   Score {game.score}")
        if not game.waveActive:
             print("Mode : EDITION")
        else:
             print("Mode : SIMULATION")

        display_dungeon(game)
        
        if game.waveActive:
            cmd = input("[Entrée] Tour suivant | [Q]uitter la vague | [R]estart : ").lower()
            if cmd == 'q':
                game.waveActive = False  # Arrêt forcé
            elif cmd == 'r':
                # Redémarrer la partie avec un nouveau donjon vierge et reset budget/score
                dungeon = Dungeon(width=10, height=10)
                game = GameState(dungeon)
                print("Partie redémarrée !")
            else:
                try:
                    res_old_nbWave, res_morts, res_tresors, res_score, res_nbWave = game.updateWave()

                    print(
                        f"\n=== FIN DE LA VAGUE {res_old_nbWave} ===\n"
                        f"Morts : {res_morts}\n"
                        f"Trésors atteints : {res_tresors}\n"
                        f"Score total : {res_score}\n"
                        f"Prochaine vague : {res_nbWave}\n"
                    )

                    if game.score < 0:
                        restart = input("=== GAME OVER ===\nSouhaitez-vous recommencer ? [O/n] ").lower()
                        if restart == "o" or restart == "":
                            game.restartGame(game.dungeon.width, game.dungeon.height)
                        else:
                            exit(0)

                except TypeError:
                    pass
                
                if not game.waveActive:
                    input("Tapez sur ENTREE pour retourner au menu d'édition") # Temps d'attente pour bien voir le message de fin de vague
                

        
        else:
            print("\nActions :")
            print("[M, P, E, B] Placer [Mur, Piege, Effacer, Bête]")
            print("Prix : Mur(20 or), Piège(10/20/30/40 or), Bête(40 or)")
            print("[L]ancer la vague | [A]meliorer | [S]auvegarder | [C]harger | [D]ifficulté | [Q]uitter")
            
            choice = input("Choix : ").lower()
            
            try:

                if choice == 's':
                    handle_save_console(game)
                elif choice == 'c':
                   handle_load_console(game)

                elif choice == 'q':
                    break

                elif choice == 'd' :
                    print("Niveaux disponibles : [E]asy, [H]ard")
                    strat = input("Niveau de la prochaine vague : ").lower()

                    while strat not in ["e", "h"]:
                        print("Le niveau de difficulté n'est pas valide")
                        strat = input("Niveau de la prochaine vague : ")

                    if strat == "e":
                        strat = Strategy.BFS
                    elif strat == "h":
                        strat = Strategy.SMART
                    game.loadStrategy(strat)
                
                elif choice == 'l':
                    game.startWave()
                    print(f"\n>>> DÉBUT DE LA VAGUE {game.nbWave} <<<\n")

                elif choice == 'r':
                    confirm = input("Redémarrer la partie ? (o/n) : ").lower()
                    if confirm == 'o':
                        game.restartGame(game.dungeon.width, game.dungeon.height)
                        print("Nouvelle partie démarrée !")
                
                elif choice == 'a':
                    print("Quel piege voulez-vous ameliorer ?")
                    print(f"[T]rou ({Hole.get_upgrade_cost(game.levels[Hole])} or), [P]ique ({Spike.get_upgrade_cost(game.levels[Spike])} or)")
                    amelioration = ""

                    while amelioration not in ['t', 'p']:
                        amelioration = input("Choix : ").lower()
                        if amelioration == 't':
                            game.upgradeTrap(Hole)
                        elif amelioration == 'p':
                            game.upgradeTrap(Spike)
                       
                        

                elif choice == 'm' or choice == 'p' or choice == 'e' or choice == 'b':

                    type_of_trap = ["t", "p", "f", "r"]
                    valid_piege = True  # Utile pour le if un peu plus bas

                    if choice == 'p':
                        print("Quel type de piège voulez-vous poser ?")
                        print("[T]rou, [P]ique, [R]une, [F]eu")
                        print(f"Prix : Trou ({Hole.get_cost(game.levels[Hole])} or), Pique ({Spike.get_cost(game.levels[Spike])} or), Rune (40 or), Feu (40 or)")
                        piege = input("Choix : ").lower()

                        if piege not in type_of_trap:
                                print("ERREUR : le piège n'existe pas !")
                                valid_piege = False

                    if valid_piege:     # Pour ne rien faire si le type de piège n'existe pas
                        
                        coord = input("Coordonnées (x,y) : ")
                        try:
                            x, y = map(int, coord.split(','))   # On sort direct du try si les coordonnées ne sont pas des int

                            if type(x)!=int or type(y)!=int :
                                print("Erreur de format. Utilisez x,y (ex: 5,5)")

                            if type(x)==int or type(y)==int :
                                match choice:
                                    case 'e':
                                        target_type = EntityType.EMPTY
                                        success_value = game.buyElement(x,y, EntityType.EMPTY, None)
                                    case 'm':
                                        target_type = EntityType.WALL
                                        success_value = game.buyElement(x, y, target_type)
                                    case 'b':
                                        target_type = EntityType.MONSTER
                                        success_value = game.buyElement(x,y,target_type, Monster(len(game.dungeon.monsters), 60, 20, (x,y), 40))
                                    case 'p':
                                        target_type = EntityType.TRAP
                                        match piege:
                                            case 'p':
                                                success_value = game.buyElement(x, y, target_type, Spike())
                                            case 't':
                                                success_value = game.buyElement(x,y,target_type, Hole())
                                            case 'r' :
                                                success_value = game.buyElement(x,y,target_type, Rune())
                                            case 'f' :
                                                success_value = game.buyElement(x,y,target_type, Fire())

                                match success_value:
                                    case 0:
                                        print("\nConstruction terminée !\n")
                                    case -1:
                                        print("\nERREUR : Opération invalide, les coordonnées entrées sont en dehors des limites du donjon !\n")
                                    case 1:
                                        print("\nERREUR : Opération invalide, la case contient un élément irremplaçable ! (Entrée ou Trésor)\n")
                                    case 2:
                                        print("\nERREUR : Budget insuffisant !\n")
                                    case 5 :
                                        print("\nERREUR ! Vous ne pouvez pas bloquer tous les chemins menant au trésor !\n")
                                    case 10:
                                        print("\nÉlément effacé !\n")
                                    case 11:
                                        print("\nERREUR : Vous ne pouvez pas effacer le contenu de cette case ! (Entrée ou Trésor)\n")
                                    case 12:
                                        print("\nLa case est déjà vide.\n")
                        except ValueError:
                            print("\nErreur de format ! Entrez \"x,y\" avec x et y des entiers (ex: 4,5)\n")
                else:
                    print("\nSélection invalide !\n")
            except ValueError:
                print("\nSélection invalide !\n")
            input("Tapez sur ENTREE pour continuer")
        
        os.system('cls' if os.name == 'nt' else 'clear') 

if __name__ == "__main__":
    main()
