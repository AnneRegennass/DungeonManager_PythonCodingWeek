import pytest
from models.dungeon import Dungeon
from models.entity import EntityType, Trap

def test_dungeon_init():
    d = Dungeon(5, 5)
    assert d.width == 5
    assert d.height == 5
    assert d.entry_pos == (0, 0)
    assert d.treasure_pos == (4, 4)

def test_is_valid_pos():
    d = Dungeon(5, 5)
    assert d.is_valid_pos(0, 0)
    assert d.is_valid_pos(4, 4)
    assert not d.is_valid_pos(-1, 0)
    assert not d.is_valid_pos(5, 5)

def test_place_wall():
    d = Dungeon(5, 5)
    assert d.placeElement(1, 1, EntityType.WALL) == 0
    assert d.get_cell(1, 1) == EntityType.WALL

def test_place_trap():
    d = Dungeon(5, 5)
    trap = Trap(10, 5, 3)
    assert d.placeElement(2, 2, EntityType.TRAP, trap) == 0
    assert d.get_cell(2, 2) == EntityType.TRAP
    assert (2, 2) in d.trap


def test_access_not_blocked():
    d = Dungeon(3, 3)
    d.placeElement(1, 0, EntityType.WALL)
    d.placeElement(1, 1, EntityType.WALL)

    error_code = d.placeElement(0, 1, EntityType.WALL)
    assert d.grid[1][0] == EntityType.EMPTY     # C'est au format d.grid[y][x]
    assert error_code == 5

    error_code = d.placeElement(0, 2, EntityType.WALL)
    assert d.grid[2][0] == EntityType.EMPTY
    assert error_code == 5