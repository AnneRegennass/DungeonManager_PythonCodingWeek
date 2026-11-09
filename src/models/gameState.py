from math import floor, ceil
from models.dungeon import *
from strategies.bfs import *
from models.entity import Hero, EntityType, COSTS, Strategy
from strategies.bfs import get_next_step_bfs
from strategies.lessDangerous import get_next_step_LessDangerous
from strategies.bfsMonstre import *
from strategies.fearless import get_next_step_Fearless
from strategies.confusedMove import *
import json
import os
import random

SOLD = 0.2
ENEMY_LOWER_SCORE = 500
ENEMY_DEATH_UPPER_SCORE = 100
BUDGET = 150

def cout_th(d1, d2):
    """
    :entrée: Dungeon d1, Dnugeon d2 
    :sortie: int
    :description: Renvoie la différence de coût pour passer de d1 à d2
    """
    c_th = 0
    # On prend la plus grande dimension pour couvrir les deux maps
    max_h = max(d1.height, d2.height)
    max_w = max(d1.width, d2.width)
    for x in range(max_h):
        for y in range(max_w):  # si on déborde on considère la case comme vide
            t1 = d1.grid[x][y] if (y < d1.height and x < d1.width) else EntityType.EMPTY
            t2 = d2.grid[x][y] if (y < d2.height and x < d2.width) else EntityType.EMPTY
            if t1 != t2:
                if t2 != EntityType.TRAP and t1 != EntityType.TRAP:
                    c_th += (COSTS.get(t2, 0) - COSTS.get(t1, 0) * SOLD)

    # Cout des nouveaux pièges dans d2
    for pos, trap2 in d2.trap.items():
        if pos not in d1.trap or d1.trap[pos].__class__ != trap2.__class__ or d1.trap[pos].level != trap2.level:
            old_trap_refund = (d1.trap[pos].cost * SOLD) if pos in d1.trap else 0
            c_th += (trap2.cost - old_trap_refund)
            
    # Remboursement pour les pièges de d1 supprimés dans d2
    for pos, trap1 in d1.trap.items():
        if pos not in d2.trap:
            c_th -= (trap1.cost * SOLD)

    return c_th

class GameState:
    def __init__(self, dungeon, budget=BUDGET): 
        self.dungeon = dungeon
        self.budget = budget
        self.score = 0
        self.waveActive = False
        self.nbWave = 1
        self.listHeros = []
        self.itWave = 0
        self.strategy = None

        self.levels = {}
        for trap in TRAP_LIST:
            self.levels[trap] = 1

    def saveGame_to_file(self, filename):
        '''
        :entrée: GameState self, String filename
        :sortie: void
        :description: Sauvegarde la partie dans un fichier ayant comme nom filename
        '''
        data = {
            "budget": self.budget,
            "score": self.score,
            "dungeon": self.dungeon.to_dict(),
            "nbWave": self.nbWave,
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def saveMap_to_file(self, filename):
        '''
        :entrée: GameState self, String filename
        :sortie: void
        :description: Sauvegarde la carte dans un fichier ayant comme nom filename
        '''
        data = {
            "type": "map_layout",
            "dungeon": self.dungeon.to_dict(),   
        }   
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename):
        '''
        :entrée: GameState self, String filename
        :sortie: int
        :description: renvoie 1 si on charge la carte sauvegarder dans filename, 2 sinon (carte non chargée, budget insuffisant).
        '''
        with open(filename, "r") as f:
            data = json.load(f)
        if "budget" in data and "score" in data and "dungeon" in data:
            self.budget = data["budget"]
            self.score = data["score"]
            self.dungeon = Dungeon.from_dict(data["dungeon"])
            self.listHeros = [] 
            self.waveActive = False
            self.nbWave = data["nbWave"]
            return 1

        # sauvegarde structure de Map 
        elif (data.get("type") == "map_layout" or "dungeon" in data):
            # On crée un objet Dungeon temporaire pour comparer
            new_dungeon = Dungeon.from_dict(data.get("dungeon"))
            c_th= cout_th(self.dungeon,new_dungeon)

            # Vérification du budget
            if self.budget >= c_th:
                self.dungeon = new_dungeon
                self.budget -= c_th
                
            else:
                raise ValueError(f"Budget insuffisant : il manque {c_th - self.budget} or.")
        return 2
    
    def buyElement(self, x, y, element_type, element=None):
        '''
        :entrée: GameState self, int x, int y, ElementType element_type, element
        :sortie: int
        :description: Permet d'acheter l'élément element à la position (x,y) et de mettre à jour self.
        '''
        if self.dungeon.is_valid_pos(x, y):
            # Calcul du coût
            if element_type != EntityType.TRAP:
                cost = COSTS[element_type]
            else:
                cost = type(element).get_cost(self.levels[type(element)])

            cellule = self.dungeon.get_cell(x, y)

            if cellule == element_type:
                if element_type == EntityType.TRAP :
                    trap_existant = self.dungeon.trap.get((x, y))
                    if type(trap_existant) == type(element):
                        # si c'est un trou on vérifie aussi son niveau
                        if not isinstance(element, Rune) and not isinstance(element, Fire):
                            if not hasattr(element, 'level') or (trap_existant.level == element.level):
                                return True 
                else:
                    return True 

            # Logique de remplacement/vente
            if cellule not in [EntityType.EMPTY, EntityType.ENTRY, EntityType.TREASURE]:
                if cellule != EntityType.TRAP:
                    cellule_cost = COSTS[cellule]
                else:
                    cellule_cost = self.dungeon.trap[(x, y)].cost
                
                benef_vente = floor(cellule_cost * SOLD)

                if self.budget + benef_vente >= cost:
                    self.budget += benef_vente
                    self.budget -= cost
                    if cellule == EntityType.TRAP:
                        self.dungeon.trap.pop((x, y))
                    elif cellule == EntityType.MONSTER:
                        self.dungeon.monsters.pop((x,y))
                    return self.dungeon.placeElement(x, y, element_type, element)
            
            elif cellule in [EntityType.ENTRY, EntityType.TREASURE]:
                if element_type == EntityType.EMPTY :
                    return 11   # Code d'erreur : on ne peut pas effacer l'entrée ou le trésor
                return 1    # Code d'erreur : on ne peut pas placer d'éléments sur l'entrée ou le trésor
            
            else:
                # Cas classique d'achat sur case vide
                if element_type != EntityType.EMPTY:
                    if self.budget >= cost:
                        placement_ok = self.dungeon.placeElement(x, y, element_type, element)
                        if placement_ok == 0 or placement_ok == 10:
                            self.budget -= cost
                        return placement_ok     # Code d'erreur 5 si tous les chemins bloqués ; 0 si tout est ok
                    else:
                        return 2    # Code d'erreur : Budget insuffisant
                else :
                    return 12   # Code d'erreur : case déjà vide
        else:
            return -1   # Code d'erreur : en dehors des limites du donjon
    
    def upgradeTrap(self, trap):
        '''
        :entrée: GameState self, Trap trap
        :sortie: bool
        :description: Renvoie si on améliore le piège trap donné en argument et l'améliore.
        '''
        if self.levels[trap] < trap.get_maxLevel() and self.budget >= trap.get_upgrade_cost(self.levels[trap]):
            self.budget -= trap.get_upgrade_cost(self.levels[trap])
            self.levels[trap] += 1
            return True
        else:
            return False

    def isFinish(self):
        '''
        :entrée: GameState self
        :sortie: bool, int, int
        :description: Renvoie bool si la partie est finie, int le nombre de héros morts, int le nombre de héros ayant atteint le trésor.
        '''
        morts = 0
        tresors = 0
        for hero in self.listHeros:
            if hero.isDead:
                morts += 1
            # Vérifie bien que l'attribut est 'reachedTreasure'
            if getattr(hero, 'reachedTreasure', False): 
                tresors += 1
        
        # La vague est finie si tous les héros sont soit morts soit au trésor
        vague_finie = (morts + tresors == len(self.listHeros)) if self.listHeros else False
        return vague_finie, morts, tresors

    def startWave(self):
        '''
        :entrée: GameState self
        :sortie: bool
        :description: Crée un liste de héros en fonction du numéro de la vague et déclenche un vague d'ennemis
        '''
        self.listHeros = []
        self.itWave = 0
        wave_modulo = self.nbWave %  5
        nb_base_heroes_added = 0
        phase_i = ceil(self.nbWave/5)
        heroes_level = phase_i
        
        # Ajout des héros de base
        if self.nbWave <= 3:
            nb_base_heroes_added = self.nbWave
        elif self.nbWave <= 5:
            nb_base_heroes_added = 3
        elif self.nbWave <= 8:
            nb_base_heroes_added = self.nbWave - 2
        else:
            nb_base_heroes_added = 6

        for j in range(nb_base_heroes_added):
            if wave_modulo == 5 and j == nb_base_heroes_added-1:
                h = self.add_hero(j, heroes_level+2, wave_modulo, True)   # Ajout du boss
            else:
                h = self.add_hero(j, heroes_level, wave_modulo, False)
            self.listHeros.append(h)

        # Ajout des héros courageux
        if self.nbWave >= 8:
            strategy_fl = Strategy.FEARLESS
            maybe_strong_fearless = random.random()
            if maybe_strong_fearless <= 0.5:           # 50% de chances d'un héros fort fearless
                current_nb_heroes = len(self.listHeros)
                h = self.add_hero(current_nb_heroes, heroes_level+1, wave_modulo, strategy_fl)
                self.listHeros.append(h)
            else:
                maybe_many_fearless = random.random()
                if maybe_many_fearless <= 0.25:      # 25% de chances d'ajout de 2 héros fearless
                    for loop in range(2):
                        current_nb_heroes = len(self.listHeros)
                        h = self.add_hero(current_nb_heroes, heroes_level, wave_modulo, strategy_fl)
                        self.listHeros.append(h)    
                        
        self.waveActive = True

    def updateWave(self):
        '''
        :entrée: GameState self
        :sortie: int, int, int, int, int
        :description: Met à jour l'état du donjon pendant la vague.
        '''
        if self.itWave < len(self.listHeros):
            self.listHeros[self.itWave].loaded = True

        for hero in self.listHeros:
            if getattr(hero, 'loaded', False) and not hero.isDead and not getattr(hero, 'reachedTreasure', False):
                x, y = hero.pos
                cellule = self.dungeon.get_cell(x, y)

                #On vérifie si les effets du héro sont toujours actif ou non
                l=len(hero.effect)
                i=0
                while i!=l:
                    if hero.effectTime[i] == 0:
                        hero.effect.pop(i)
                        hero.effectTime.pop(i)
                        l-=1
                    else:
                        i+=1

                combat = []

                for i in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
                    if self.dungeon.is_valid_pos(i[0], i[1]):
                        if self.dungeon.get_cell(i[0],i[1]) == EntityType.MONSTER:
                            combat.append(i)

                if self.dungeon.get_cell(hero.pos[0],hero.pos[1]) == EntityType.TREASURE:
                    hero.reachedTreasure = True
                
                elif cellule == EntityType.TRAP:
                    trap = self.dungeon.trap.get((x, y))
                    if isinstance(trap, Rune) or isinstance(trap, Fire):
                        self.dungeon.trap[(x,y)].applyEffect(hero)
                    if trap:
                        hero.take_damage(trap.damage)
                        trap.used()
                        if hero.hp <= 0:
                            hero.hp, hero.isDead = 0, True
                        if trap.nbUse <= 0:
                            self.dungeon.trap.pop((x, y), None)
                            self.dungeon.grid[y][x] = EntityType.EMPTY

                if len(combat)>0 :
                    #le hero est en combat et ne bouge donc pas
                    i = 0
                    l = len(self.dungeon.monsters)

                    if l!=0:
                        positions = list(self.dungeon.monsters.keys())

                    while i != l:

                        monstre = self.dungeon.monsters[positions[i]]
                        if positions[i] in combat:
                            hero.take_damage(monstre.damage)
                            monstre.take_damage(hero.damage)
                        
                        if monstre.hp <= 0 :
                            monstre.isDead = True
                            xm, ym = monstre.pos
                            self.dungeon.grid[ym][xm] = EntityType.EMPTY
                            self.dungeon.monsters.pop(monstre.pos)
                            positions.pop(i)
                            l-=1
                        else :
                            i+=1

                else :
                    if Effects.CONFUSED not in hero.effect:
                        if hero.strategy == Strategy.BFS:
                            hero.pos = get_next_step_bfs(self, hero.pos, self.dungeon.treasure_pos)
                        elif hero.strategy == Strategy.FEARLESS:
                            hero.pos = get_next_step_Fearless(self, hero.pos, self.dungeon.treasure_pos)
                        else:
                            hero.pos = get_next_step_LessDangerous(self, hero.pos, self.dungeon.treasure_pos)
                    else :
                        hero.pos = confused_move(self, hero.pos)

                for i in range (len(hero.effect)):
                    hero.effectTime[i] -= 1
                    if Effects.FIRE == hero.effect[i]:
                        hero.take_damage(Fire().give_delay_damage())

        fini, morts, tresors = self.isFinish()
        if fini and self.waveActive:
            self.score += (morts * ENEMY_DEATH_UPPER_SCORE) - (tresors * ENEMY_LOWER_SCORE)
            self.waveActive = False
            old_nbWave = self.nbWave
            self.nbWave += 1

            for h in self.listHeros:
                if h.isDead:
                    self.budget += h.convert_to_money()
            
            return old_nbWave, morts, tresors, self.score, self.nbWave


        # Mouvement des monstres

        l = len(self.dungeon.monsters)
        if l>0:
            posMonstres = list(self.dungeon.monsters.keys())
            i=0
            while i != l:
                if self.dungeon.monsters[posMonstres[i]].canMove(self):
                    xav, yav = self.dungeon.monsters[posMonstres[i]].pos
                    xap, yap = get_next_step_bfs_monstre(self, self.dungeon.monsters[posMonstres[i]].pos)
                    self.dungeon.grid[yav][xav] = EntityType.EMPTY
                    self.dungeon.grid[yap][xap] = EntityType.MONSTER
                    self.dungeon.monsters[posMonstres[i]].move((xap,yap))
                    self.dungeon.monsters[(xap,yap)]= self.dungeon.monsters.pop((xav,yav))
                i+=1

        self.itWave += 1
        
        return False

    def restartGame(self, width, height, budget=100):
        '''
        :entrée: GameState self, int width, int height, int budget
        :sortie: void
        ;description: Permet de redémarrer/réinitialiser une partie
        '''
        
        self.dungeon = Dungeon(width, height)
        self.budget = budget
        self.score = 0
        self.waveActive = False
        self.nbWave = 1
        self.listHeros = []
        self.itWave = 0

        self.levels = {}
        for trap in TRAP_LIST:
            self.levels[trap] = 1

    def loadStrategy(self, strategy):
        '''
        :entrée: GameState self, Strategy strategy
        :sortie: void
        :description: Change la stratégie de self en strategy.
        '''
        self.strategy = strategy

    def get_loaded_heros(self):
        '''
        :entrée: GameState self
        :sortie: list<Hero>
        :description: Renvoie la liste des héros de self qui sont dans le donjon.
        '''
        return [h for h in self.listHeros if h.loaded]
    
    def is_hero_on(self, x, y):
        '''
        :entrée: GameState self, int x, int y
        :sortie: bool
        :descrption: Renvoie si un hero est sur la case (x,y) du donjon self.
        '''
        if self.dungeon.treasure_pos[0] == x and self.dungeon.treasure_pos[1] == y:
            return False
        for h in self.listHeros:
            if h.pos == (x, y) and not h.isDead: return True
        return False
    
    def add_hero(self, j, lvl, wave_modulo, boss, strategy=Strategy.BFS):

        if self.strategy != None:
            strategy = self.strategy

        hp = 100 + (lvl - 1) * 50
        dmg = 20 + (lvl - 1) * 10

        # Gestion des buff
        match wave_modulo:
            case 4:
                chance_buff = 0.8
            case 0:
                chance_buff = 0.6
            case _:
                chance_buff = -1

        maybe_hp_buff = random.random()
        maybe_damage_buff = random.random()

        if maybe_hp_buff <= chance_buff:
            hp += hp*0.3
        if maybe_damage_buff <= chance_buff:
            dmg += dmg*0.3

        # Gestion de la stratégie
        if self.nbWave > 5:
            if strategy != Strategy.FEARLESS:
                maybe_smart = random.random() - 0.02 * (self.nbWave-6)  # On rajoute 2% de chances d'être smart chaque vague
                if maybe_smart <= 0.5:
                    strategy = Strategy.SMART

        h = Hero(j, hp, dmg, self.dungeon.entry_pos, strategy, boss=boss)
        return h
    
    def is_monster_on(self, x, y):
        '''
        :entrée: GameState self, int x, int y
        :sortie: Bool ou Monster
        :description: Renvoie le monstre dans le donjon self aux coordonnées (x,y) s'il y en a un.
        '''
        return self.dungeon.monsters.get((x, y))
