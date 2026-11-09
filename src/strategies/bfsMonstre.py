from collections import deque
from models.entity import *
from random import shuffle

def get_next_step_bfs_monstre(game, start_pos):
    '''
    :entrée: GameState game, tuple<int> start_pos
    :sortie: tuple<int>
    :description: Réalise un parcours en largeur entre le monstre en start_pos et le héro le plus proche de lui. Si il n'y a pas de héro, on renvoie start_pos.
    '''
    queue = deque()
    queue.append(start_pos)
    
    came_from = {start_pos: None}
    
    found = False

    while queue:
        current = queue.popleft()

        for hero in game.listHeros :
            if current == hero.pos:
                found = True
                target_pos = current
                break

        x, y = current
        neighbors = [
            (x, y - 1), (x, y + 1), # Haut, Bas
            (x - 1, y), (x + 1, y)  # Gauche, Droite
        ]

        shuffle(neighbors)

        for next_pos in neighbors:
            nx, ny = next_pos
            
            # si c'est des voisins valide, on essaiera d'y accéder
            if (game.dungeon.is_valid_pos(nx, ny) and 
                next_pos not in came_from and 
                game.dungeon.get_cell(nx, ny) not in[EntityType.TRAP, EntityType.WALL, EntityType.ENTRY, EntityType.TREASURE] and
                not game.is_monster_on(nx, ny)):
                
                queue.append(next_pos)
                came_from[next_pos] = current

    # Si aucun chemin n'a été trouvé (bloqué par des murs)
    if not found:
        return start_pos # Le héros reste sur place

    # on reconstruit le chemin
    step = target_pos
    while came_from[step] != start_pos:
        step = came_from[step]

        if step is None:
            return start_pos
    return step # C'est la première case après le départ

