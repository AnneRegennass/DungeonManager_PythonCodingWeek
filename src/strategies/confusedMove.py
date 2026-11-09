from models.entity import Hero, Effects, EntityType
from random import randint

def confused_move(game, start_pos):
    '''
    :entrée: GameState game, tuple<int> start_pos
    :sortie: tuple<int>
    :description: Fait bouger aléatoirement le héro en start_pos autour de lui.
    '''
    x , y = start_pos
    pos_possibles = []
    for pos in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
        i,j = pos
        if game.dungeon.is_valid_pos(i,j) and game.dungeon.get_cell(i,j) != EntityType.WALL :
                pos_possibles.append(pos)
    k = len(pos_possibles)
    if k>0:
         return pos_possibles[randint(0,k-1)]
    return start_pos
