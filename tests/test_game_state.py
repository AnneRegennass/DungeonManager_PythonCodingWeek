from models.dungeon import Dungeon
from models.gameState import GameState
from models.entity import EntityType, Trap, Hero, Spike
from math import inf

def test_buy_wall():
    d = Dungeon(5, 5)
    game = GameState(d, budget=50)
    success = game.buyElement(1, 1, EntityType.WALL)
    assert success == 0
    assert game.budget == 30

def test_buy_wall_not_enough_money():
    d = Dungeon(5, 5)
    game = GameState(d, budget=10)
    success = game.buyElement(1, 1, EntityType.WALL)
    assert success == 2
    assert game.budget == 10

def test_buy_and_sell_trap():
    d = Dungeon(5, 5)
    game = GameState(d, budget=50)
    trap = Spike()
    game.buyElement(1, 1, EntityType.TRAP, trap)
    old_budget = game.budget

    game.buyElement(1, 1, EntityType.EMPTY)
    assert game.budget > old_budget

def test_buy_out_of_bounds():
    d = Dungeon(5, 5)
    game = GameState(d, budget=50)
    assert game.buyElement(10, 10, EntityType.WALL) == -1

def test_start_wave():
    d = Dungeon(5, 5)
    game = GameState(d, budget=50)
    game.startWave()
    assert game.waveActive
    assert len(game.listHeros) == 1
    assert game.nbWave == 1
    assert game.listHeros[0].pos == d.entry_pos

def test_start_second_wave():
    d = Dungeon(5, 5)
    vertical_step = d.height-1
    horizontal_step = d.width-1
    game = GameState(d, budget=50)
    game.startWave()
    for loop in range(vertical_step+horizontal_step+1):
        game.updateWave()
    assert game.isFinish()[0]
    game.startWave()
    assert game.waveActive
    assert len(game.listHeros) == 2
    assert game.nbWave == 2
    assert game.listHeros[0].pos == d.entry_pos
    assert game.listHeros[1].pos == d.entry_pos
   

def test_wave_ends_when_hero_reaches_treasure():
    d = Dungeon(2, 2)
    game = GameState(d, budget=50)
    game.startWave()

    hero = game.listHeros[0]
    hero.pos = d.treasure_pos
    hero.reachedTreasure = True

    fin, mort, tresor = game.isFinish()
    assert tresor

def test_score_penalty_when_treasure_reached():
    d = Dungeon(2, 2)
    game = GameState(d, budget=50)
    game.startWave()

    hero = game.listHeros[0]
    hero.pos = d.treasure_pos
    hero.reachedTreasure = True

    game.updateWave()
    assert game.score < 0

def test_trap_exhaustion():
    d = Dungeon(3, 3)
    game = GameState(d, budget=100)
    # Piège qui ne marche qu'une fois
    trap = Spike()
    game.buyElement(1, 0, EntityType.TRAP, trap)
    
    # On crée un héros manuel
    hero = Hero(id=1, hp=100, damage=0, start_pos=(0, 0))
    game.listHeros = [hero]
   
    # Tour 1 : Le héros marche sur le piège
    hero.pos = (1, 0)
    game.updateWave() # simule l'interaction
    assert hero.hp == 80
    assert trap.nbUse == inf
   
    # Tour 2 : Il marche encore dessus (ou un autre héros)
    hero.hp = 100
    game.updateWave()
    assert hero.hp == 100 # Ne doit plus prendre de dégâts

def test_restart_game_creates_new_dungeon():
    game = GameState(Dungeon(5, 5), 50)
    game.score = 100
    game.nbWave = 3

    game.restartGame(10, 10, 200)

    assert game.dungeon.width == 10
    assert game.dungeon.height == 10
    assert game.score == 0
    assert game.nbWave == 1
    assert game.budget == 200

