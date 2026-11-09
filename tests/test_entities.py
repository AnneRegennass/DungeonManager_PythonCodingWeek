from models.entity import (
    EntityType, Strategy,
    Trap, Spike,
    Hole,
    Hero, Monster
)
from math import inf

def test_entitytype_values():
    assert EntityType.EMPTY == 0
    assert EntityType.WALL == 1
    assert EntityType.ENTRY == 2
    assert EntityType.TREASURE == 3
    assert EntityType.TRAP == 4
    assert EntityType.HERO == 5
    assert EntityType.MONSTER == 6

def test_strategy_values():
    assert Strategy.BFS == 0
    assert Strategy.SMART == 1

# -------- TRAPS --------

def test_trap_usage_decrements_nbUse():
    trap = Trap(cost=10, damage=5, nbUse=2)
    trap.used()
    assert trap.nbUse == 1

def test_trap_usage_does_not_decrement_infinite():
    trap = Trap(cost=10, damage=5, nbUse=inf)
    trap.used()
    assert trap.nbUse == inf

def test_spike_has_infinite_usage():
    spike = Spike()
    assert spike.nbUse == inf

def test_small_hole_defaults():
    hole = Hole(level=1)
    assert hole.cost == 10
    assert hole.damage == inf
    assert hole.nbUse == 1

def test_medium_hole_defaults():
    hole = Hole(level=2)
    assert hole.cost == 20
    assert hole.damage == inf
    assert hole.nbUse == 2

def test_big_hole_defaults():
    hole = Hole(level=3)
    assert hole.cost == 30
    assert hole.damage == inf
    assert hole.nbUse == 3


# -------- HERO --------

def test_hero_default_strategy():
    hero = Hero(id=1, hp=100, damage=10, start_pos=(0, 0))
    assert hero.strategy == Strategy.BFS

def test_hero_custom_strategy():
    hero = Hero(id=2, hp=100, damage=10, start_pos=(0, 0), strategy=Strategy.SMART)
    assert hero.strategy == Strategy.SMART

def test_hero_take_damage_and_death():
    hero = Hero(id=3, hp=10, damage=5, start_pos=(0, 0))
    hero.take_damage(15)
    assert hero.isDead

def test_hero_move():
    hero = Hero(id=4, hp=20, damage=5, start_pos=(0, 0))
    hero.move((2, 3))
    assert hero.pos == (2, 3)

