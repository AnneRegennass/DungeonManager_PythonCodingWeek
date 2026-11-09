from enum import IntEnum
from math import inf
from random import randint

class EntityType(IntEnum):
    EMPTY = 0
    WALL = 1
    ENTRY = 2
    TREASURE = 3
    TRAP = 4
    HERO = 5
    MONSTER = 6

class Strategy(IntEnum):
    BFS = 0
    SMART = 1
    FEARLESS = 2

COSTS = {
    # Coût des entités pour les ajouter au donjon
    # Les éléments obligatoires sont gratuits :
    EntityType.EMPTY : 0,
    EntityType.ENTRY : 0,
    EntityType.TREASURE : 0,
    # Et ceux optionnels sont payants :
    EntityType.WALL : 20,
    EntityType.TRAP : 10,
    EntityType.MONSTER : 40,
}

class Effects(IntEnum):
    FIRE = 1
    CONFUSED = 2

class Trap:

    def __init__(self, cost, damage, nbUse, level=1):
        self.cost = cost
        self.damage = damage
        self.nbUse = nbUse
        self.level = level
        self.upgradeCost = 0

    def used(self):
        '''
        :entrée: Trap self
        :sortie: void
        :description: Utilise un piège (fait diminuer de 1 son nombre d'utilisations restantes)
        '''
        if self.nbUse != inf :
            self.nbUse -= 1

class Spike(Trap):
    @staticmethod
    def get_maxLevel():
        '''
        :entrée: Spike self
        :sortie: int
        :description: Renvoie le niveau maximal des piques.
        '''
        return 5
    
    @staticmethod
    def get_cost(level):
        '''
        :entrée: Spike self, int level
        :sortie: int
        :description: Renvoie le coût d'achat du pique.
        '''
        return int(10*(1 + (level-1)*0.3))
    
    @staticmethod
    def get_upgrade_cost(level):
        '''
        :entrée: Spike self, int level
        :sortie: int
        :description: Renvoie le coût d'amélioration des piques.
        '''
        return 3*Spike.get_cost(level)

    def __init__(self, level=1):
        '''
        :entrée: Spike self, int level
        :sortie: void
        :description: Crée un pique.
        '''
        cost = 10*(1 + (level-1)*0.3)
        damage = 20*(1 + (level-1)*0.3)
        nbUse = inf
        self.upgradeCost = 50+((level-1)*15)
        super().__init__(cost, damage, inf, level)
    
    def change_level(self, new_level):
        '''
        :entrée: Spike self, int new_level
        :sortie: void
        :description: Change le niveau de self en new_level
        '''
        self.level = new_level
        self.__init__(new_level)


class Fire(Trap):

    @staticmethod
    def get_cost(level=1):
        '''
        :entrée: Fire self, int level
        :sortie: int
        :description: Renvoie le prix d'achat d'un Feu
        '''
        return 40

    def __init__(self, cost = 40, damage = 10, nbUse = inf, level = 1):
        super().__init__(cost, damage, nbUse, level)
    
    def applyEffect(self, hero):
        '''
        :entrée: Fire self, Hero hero
        :sortie: void
        :description: Ajoute l'effet de Feu au héro hero.
        '''
        hero.effect.append(Effects.FIRE)
        (hero.effectTime).append(10)

    def give_delay_damage(self):
        '''
        :entrée: Fire self
        :sortie: int
        :description: Renvoie les dégats infligés aux héros enflammés.
        '''
        return int(self.damage/2)

class Rune(Trap):

    @staticmethod
    def get_cost(level=1):
        '''
        :entrée: Rune self
        :sortie: int
        :description: Renvoie le coût d'achat d'une rune.
        '''
        return 40

    def __init__(self, cost = 40, damage = 0, nbUse = inf, level =1):
        super().__init__(cost, damage, nbUse, level)

    def applyEffect(self, hero):
        '''
        :entrée: Rune self, Hero hero
        :sortie: void
        :description: Ajoute l'effet de Confus au héro hero.
        '''
        hero.effect.append(Effects.CONFUSED)
        hero.effectTime.append(8)

class Hole(Trap):
    
    @staticmethod
    def get_maxLevel():
        '''
        :entrée: Hole self
        :sortie: int
        :description: Renvoie le niveau maximal d'un trou.
        '''
        return 3
    
    @staticmethod
    def get_cost(level):
        '''
        :entrée: int level
        :sortie: int
        :description: Renvoie le coût d'achat d'un trou en fonction de son niveau.
        '''
        return 20*level
    
    @staticmethod
    def get_upgrade_cost(level):
        '''
        :entrée: int level
        :sortie: int
        :description: Renvoie le coût d'amélioration d'un trou.
        '''
        return int(20+Hole.get_cost(level))
    
    def __init__(self, level=1):
        cost = 10*level
        damage=inf
        nbUse = level
        self.upgradeCost = 50+((level-1)*40)
        super().__init__(cost, damage, nbUse, level)

    def change_level(self, new_level):
        '''
        :entrée: Hole self, int new_level
        :sortie: void
        :description: Met à jour le niveau de self à new_level
        '''
        self.level = new_level
        self.__init__(new_level)

class Hero:
    def __init__(self, id, hp, damage, start_pos, strategy=Strategy.BFS, effect=None, time=None, boss=False):
        self.id = id
        self.pos = start_pos
        self.maxHp = hp
        self.hp = hp
        self.damage = damage
        self.isDead = False
        self.reachedTreasure = False
        self.strategy = strategy
        self.effect = []
        self.effectTime = []
        self.boss = boss
        self.loaded = False # il est visible et en jeu sur le terrain
    
    def take_damage(self, amount):
        '''
        :entrée: Hero self, int amount
        :sortie: void
        :description: Inflige des dégats de amount à self.
        '''
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0 # On évite les HP négatifs
            self.isDead = True

    def move(self, new_pos):
        '''
        :entrée: Hero self, tuple<int> new_pos
        :sortie: void
        :description: Change la position de self à new_pos
        '''
        # Si le héros est mort, il ne devrait plus bouger
        if not self.isDead:
            self.pos = new_pos
    
    def convert_to_money(self):
        '''
        :entrée: Hero self
        :sortie: int
        :description: Calcule le nombre d'or obtenu en tuant le héro self.
        '''
        return int(
            self.maxHp*0.1 +
            self.damage*0.5 +
            (20 if self.strategy == Strategy.SMART else 10 if self.strategy == Strategy.FEARLESS else 0) +
            randint(0, 20)
        )

class Monster:
    def __init__(self, id, hp, damage, start_pos, cost):
        self.id = id
        self.pos = start_pos
        self.maxHp = hp
        self.hp = hp
        self.damage = damage
        self.isDead = False
        self.cost = cost

    def take_damage(self, amount):
        '''
        :entrée: Monster self, int amount
        :sortie: int
        :description: Inflige des dégats de amount à self. 
        '''
        self.hp -= amount
        if self.hp <=0:
            self.isDead = True

    def move(self, new_pos):
        '''
        :entrée: Monster self, tuple<int> new_pos
        :sortie: void
        :description: Change la position de self à new_pos
        '''
        self.pos = new_pos

    def canMove(self, game):
        '''
        :entrée: Monster self, GameState game
        :sortie: bool
        :description: Renvoie si le monstre self peut bouger (s'il combat ou non un héro).
        '''
        x,y = self.pos
        for i in game.listHeros :
            if i.pos in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                # le monstre est dans un combat (hero à proximité de lui) donc il ne bouge pas
                return False
        return True


TRAP_LIST = [Hole, Spike, Rune, Fire]