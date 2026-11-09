import heapq


from models.entity import *
from models.dungeon import *
from strategies.lessDangerous import get_next_step_LessDangerous
from random import shuffle

def get_next_step_Fearless(game, start_pos,target_pos):
    '''
    :entrée: GameState game, tuple<int> start_pos, tuple<int> target_pos
    :sortie: tuple<int>
    :description: Fait bouger le héro en start_pos vers le monstre le plus proche. Si il n'y a pas de monstre, il se dirige vers target_pos.
    '''
    if start_pos == target_pos:  #si on est au trésor c'est fini   
        return start_pos
    dungeon = game.dungeon

    # Trouver tous les monstres vivants
    targets = [pos for pos, m in dungeon.monsters.items() if not m.isDead]
 

    # Si aucun monstre, on reprend la strategie lessDangerous
    if not targets:
        return get_next_step_LessDangerous(dungeon, start_pos, dungeon.treasure_pos)
    
    heap = [(0, start_pos)]
    came_from = {start_pos: None}
    danger = {start_pos: 0}
    found_target = None

    while heap:
        current_danger, current = heapq.heappop(heap)
        
        #si on trouve un monstre on s'arrete
        if current in targets:
            found_target = current
            break
    
        x, y = current
        parcours = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        shuffle(parcours)
        for dx, dy in parcours:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)


            if 0 <= nx < dungeon.width and 0 <= ny < dungeon.height and dungeon.get_cell(nx, ny) != EntityType.WALL:
                
                cell_type = dungeon.get_cell(nx, ny) 
                new_danger = current_danger + 1 # Calcul du coût (on évite les pièges): coût de base pour avancer

                if cell_type == EntityType.TRAP:
                    trap = dungeon.trap.get(next_pos)
                    new_danger += trap.damage if trap else 0
                
                if next_pos not in danger or new_danger < danger[next_pos]:
                    danger[next_pos] = new_danger
                    came_from[next_pos] = current
                    heapq.heappush(heap, (new_danger, next_pos))


    # Si on n'a rien trouvé, on va au trésor
    if not found_target:
        return get_next_step_LessDangerous(dungeon, start_pos, target_pos)
    
    # on reconstruit le chemin
    step = found_target
    while came_from[step] != start_pos:
        step = came_from[step]
        if step is None:
            return start_pos
    return step # C'est la première case après le départ