
import sys
import os

# Ajout dynamique des chemins pour éviter les ModuleNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
src_path = os.path.join(project_root, 'src')

sys.path.append(project_root)
sys.path.append(src_path)

from models.gameState import *
from models.dungeon import Dungeon
from models.entity import *
from strategies.bfs import get_next_step_bfs
from strategies.lessDangerous import get_next_step_LessDangerous
from strategies.lessDangerous import get_next_step_LessDangerous
from strategies.fearless import get_next_step_Fearless
from strategies.bfsMonstre import get_next_step_bfs_monstre


# Objet Mock pour simuler le GameState sans lancer tout le jeu
class MockGame:
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.listHeros = []

    def is_monster_on(self,x, y):
        return self.dungeon.monsters.get((x, y))
    
# 1. TESTS STRATÉGIE BFS 

def test_bfs_basic_path():
    """Test de base : chemin le plus court sans obstacle"""
    d = Dungeon(5, 5, 0, 0, 2, 0)
    step = get_next_step_bfs(d, (0, 0), (2, 0))
    assert step == (1, 0) # Doit avancer tout droit

def test_bfs_blocked_by_wall():
    """Vérifie que le BFS contourne un mur"""
    d = Dungeon(3, 3, 0, 0, 2, 0)
    d.grid[0][1] = EntityType.WALL # Mur entre (0,0) et (2,0)
    step = get_next_step_bfs(d, (0, 0), (2, 0))
    assert step == (0, 1) # Doit descendre pour contourner

def test_bfs_ignores_monsters():
    """BFS ne considère pas les monstres comme des obstacles bloquants"""
    d = Dungeon(3, 3, 0, 0, 2, 0)
    d.grid[0][1] = EntityType.MONSTER # Un monstre est sur le chemin
    step = get_next_step_bfs(d, (0, 0), (2, 0))
    assert step == (1, 0) # Traverse la case du monstre car ce n'est pas un mur



# 2. TESTS STRATÉGIE LESS DANGEROUS 


def test_less_dangerous_avoids_spike():
    """Vérifie que le héros contourne un piège qui fait trop de dégâts"""
    d = Dungeon(3, 3, 0, 0, 2, 0)
    # Piège mortel en (1,0)
    d.placeElement(1, 0, EntityType.TRAP, Spike(level=10))
    step = get_next_step_LessDangerous(d, (0, 0), (2, 0))
    assert step == (0, 1) # Choisit le chemin sûr même s'il est plus long

def test_less_dangerous_accepts_trap():
    """Le héros peut choisir un piège si le détour est impossible (ou si le danger est minime)"""
    d = Dungeon(3, 3, 0, 0, 2, 0)
    # On bloque tout sauf le passage par le piège
    d.grid[1][0] = EntityType.WALL
    d.grid[1][1] = EntityType.WALL
    d.placeElement(1, 0, EntityType.TRAP, Hole())
    
    step = get_next_step_LessDangerous(d, (0, 0), (2, 0))
    assert step == (1, 0) # il marche sur le trou


def test_less_dangerous_complex_path():
    d = Dungeon(5, 5)
    d.placeElement(1, 0, EntityType.TRAP, Trap(10,10,3)) 

    step = get_next_step_LessDangerous(d, (0, 0), (2, 0))
    assert step == (0, 1)


   #3. TESTS STRATÉGIE FEARLESS


def test_hero_targets_closest_monster():
    """Le hero doit aller vers le monstre, pas vers le trésor"""
    d = Dungeon(5, 5, 0, 0, 4, 4) # Trésor très loin
    d.grid[0][2] = EntityType.MONSTER # Monstre tout près
    d.monsters[(2,0)] = Monster(1, 50, 10, (2,0), 100)
    
    game = MockGame(d)
    step = get_next_step_Fearless(game, (0, 0), (4, 4))
    assert step == (1,0) # Se dirige vers le monstre 


def test_hero_avoids_trap_to_reach_monster():
    """Le hero évite les pièges """
    d = Dungeon(5, 5, 0, 0, 4, 4)
    d.grid[0][2] = EntityType.MONSTER
    d.monsters[(2,0)] = Monster(1, 50, 10, (2,0), 100)
    # Piège sur le chemin direct
    d.placeElement(1,0, EntityType.TRAP, Spike())
    
    game = MockGame(d)
    start_pos = (0, 0)
    target_pos = (4, 4)

    step = get_next_step_Fearless(game, start_pos, target_pos)
    assert step == (0, 1) # Fait un détour pour ne pas mourir avant d'arriver au monstre

def test_hero_fallback_to_treasure():
    """Si aucun monstre n'est vivant, le hero va au trésor"""
    d = Dungeon(5, 5, 0, 0, 0, 2)
    # Liste de monstres vide
    game = MockGame(d)
    start_pos = (0, 0)
    target_pos = (4, 4)

    step = get_next_step_Fearless(game,start_pos, target_pos)
    assert step == (0, 1) # Va vers le trésor en (0,2) 


 #4. TESTS STRATÉGIE MONSTRE (BFS Monstre)

def test_monstre_targets_hero():
    """Le monstre doit trouver le héros le plus proche"""
    d = Dungeon(5, 5)
    game = MockGame(d)
    # On ajoute un héros en (2,0)
    game.listHeros = [Hero('H',100,10,(2,0))]
    
    step = get_next_step_bfs_monstre(game, (0, 0))
    assert step == (1, 0) # Le monstre avance vers le héros


if __name__ == "__main__":
    try:
        print("Lancement des tests...")
        test_bfs_basic_path()
        test_bfs_blocked_by_wall()
        test_bfs_ignores_monsters()
        test_less_dangerous_avoids_spike()
        test_less_dangerous_accepts_trap()
        test_hero_targets_closest_monster()
        test_hero_avoids_trap_to_reach_monster()
        test_hero_fallback_to_treasure()
        test_monstre_targets_hero()
        print("Tous les tests sont passés avec succès !")
    except AssertionError as e:
        print(f"Échec d'un test ! Une assertion a échoué.")
    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")