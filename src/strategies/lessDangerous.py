import heapq
from models.entity import EntityType
from random import shuffle


def get_next_step_LessDangerous(game, start_pos, target_pos):
    '''
    :entrée: GameState game, tuple<int> start_pos, tuple<int> target_pos
    :sortie: tuple<int>
    :description: Réalise un parcours en largeur pour trouver le chemin infligeant le moins de dégat de start_pos à target_pos. Renvoi la première position où aller. Si le déplacement n'est pas possible, on renvoie start_pos.
    '''
    dungeon = game.dungeon if hasattr(game, 'dungeon') else game
    
    if start_pos == target_pos:
        return start_pos

    heap = [(0, start_pos)]
    came_from = {start_pos: None}
    danger = {start_pos: 0}
    found = False

    while heap:
        current_danger, current = heapq.heappop(heap)
        if current == target_pos:
            found = True
            break

        x, y = current
        parcours = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        shuffle(parcours)
        for dx, dy in parcours:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)

            if dungeon.is_valid_pos(nx, ny) and dungeon.get_cell(nx, ny) != EntityType.WALL:
                # Calcul du danger (pièges)
                cell_type = dungeon.get_cell(nx, ny)
                cost_move = 0
                if cell_type == EntityType.TRAP:
                    trap = dungeon.trap.get(next_pos)
                    cost_move = trap.damage if trap else 0
                
                new_danger = current_danger + cost_move
                if next_pos not in danger or new_danger < danger[next_pos]:
                    danger[next_pos] = new_danger
                    came_from[next_pos] = current
                    heapq.heappush(heap, (new_danger, next_pos))

    if not found or target_pos not in came_from:
        return start_pos

    step = target_pos
    while came_from[step] != start_pos:
        step = came_from[step]
    return step