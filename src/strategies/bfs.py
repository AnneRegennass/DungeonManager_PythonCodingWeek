from collections import deque
from models.entity import EntityType
from random import shuffle

def get_next_step_bfs(game, start_pos, target_pos):
    '''
    :entrée: GameState game , tuple<int> start_pos, tuple<int> target_pos
    :sortie: tuple<int>
    :description: Réalise un parcours en largeur pour trouver le chemin le plus cours de start_pos à target_pos. Renvoi la première position où aller. Si le déplacement n'est pas possible, on renvoie start_pos.
    '''
    dungeon = game.dungeon if hasattr(game, 'dungeon') else game
    
    if start_pos == target_pos:
        return start_pos

    queue = deque([start_pos])
    came_from = {start_pos: None}
    found = False

    while queue:
        current = queue.popleft()
        if current == target_pos:
            found = True
            break

        x, y = current
        parcours = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        shuffle(parcours)
        for dx, dy in parcours:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            
            if (dungeon.is_valid_pos(nx, ny) and 
                next_pos not in came_from and 
                dungeon.get_cell(nx, ny) != EntityType.WALL):

                if hasattr(game, 'is_hero_on') and game.is_hero_on(nx, ny):
                    continue

                queue.append(next_pos)
                came_from[next_pos] = current

    step = target_pos
    if step not in came_from: return start_pos
    
    while came_from[step] != start_pos:
        step = came_from[step]
        if step is None: return start_pos
    return step