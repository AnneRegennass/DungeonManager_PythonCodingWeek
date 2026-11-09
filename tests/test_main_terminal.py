from models.entity import (
    EntityType,
    Hole, Trap, Rune, Fire
)
from mainTerminal import entity_to_chr


def test_entity_to_chr_basic_entities():
    assert entity_to_chr(EntityType.EMPTY, None) == "."
    assert entity_to_chr(EntityType.WALL, None) == "#"
    assert entity_to_chr(EntityType.ENTRY, None) == "E"
    assert entity_to_chr(EntityType.TREASURE, None) == "T"
    assert entity_to_chr(EntityType.HERO, None) == "H"
    assert entity_to_chr(EntityType.MONSTER, None) == "M"


def test_entity_to_chr_traps():
    assert entity_to_chr(EntityType.TRAP, Hole(level=1)) == "°"
    assert entity_to_chr(EntityType.TRAP, Hole(level=2)) == "o"
    assert entity_to_chr(EntityType.TRAP, Hole(level=3)) == "O"
    assert entity_to_chr(EntityType.TRAP, Rune()) == "@"
    assert entity_to_chr(EntityType.TRAP, Fire()) == "F"


def test_entity_to_chr_other_trap():
    trap = Trap(cost=10, damage=5, nbUse=2)
    assert entity_to_chr(EntityType.TRAP, trap) == "^"

