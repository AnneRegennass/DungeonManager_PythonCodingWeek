from models.entity import *

WIDTH = 32
HEIGHT = 32
class Dungeon :
    def __init__(self, width=WIDTH, height=HEIGHT, entry_pos_x=-1, entry_pos_y=-1, treasure_pos_x=-1, treasure_pos_y=-1):
        self.width = width
        self.height = height
        self.grid = [[EntityType.EMPTY for _ in range (width)] for _ in range (height)]
        self.trap = {}
        self.monsters = {}

        if entry_pos_x == -1 or entry_pos_y == -1:
            self.grid[0][0] = EntityType.ENTRY
            self.entry_pos = (0, 0)
        else:
            self.entry_pos = (entry_pos_x, entry_pos_y)
            self.grid[entry_pos_y][entry_pos_x] = EntityType.ENTRY
        
        if treasure_pos_x == -1 or treasure_pos_y == -1:
            self.grid[height-1][width-1] = EntityType.TREASURE
            self.treasure_pos = (width-1, height-1)
        else:
            self.treasure_pos = (treasure_pos_x, treasure_pos_y)
            self.grid[treasure_pos_y][treasure_pos_x] = EntityType.TREASURE
        
    def is_valid_pos(self, x, y):
        '''
        :entrée: Dungeon self, int x, int y
        :sortie: bool
        :description: Renvoie si les coordonnées données appartiennent au donjon
        '''
        return 0 <= x < self.width and 0 <= y < self.height
    
    def placeElement(self, x, y, element_type, element=None):
        '''
        :entrée: Dungeon self, int x, int y, EntityType element_type, element
        :sortie: int 
        :description: pour des coordonnées (x,y) valides, renvoie 10 si on pose une case vide, 5 si le placement n'est pas possible (si tous les chemins sont bloqués), 0 si le placement est effectué avec succès.
        '''

        # On entre jamais dans la fonction si x,y ne sont pas des coordonnées valides (cf. f° buyElement)

        self.grid[y][x] = element_type

        if element_type == EntityType.EMPTY:
            return 10

        # Vérification qu'on ne bloque pas tous les chemins vers le trésor
        if element_type == EntityType.WALL:
            already_visited = [(self.entry_pos)]

            if not self.there_is_a_way(self.entry_pos[0],self.entry_pos[1],self.treasure_pos[0],self.treasure_pos[1],already_visited):
                self.grid[y][x] = EntityType.EMPTY
                # Code d'erreur : tous les chemins bloqués
                return 5  


        if element_type == EntityType.TRAP :
            self.trap[(x,y)] = element

        if element_type == EntityType.MONSTER :
            self.monsters[(x,y)] = element
        
        return 0

    def get_cell(self, x, y):
        '''
        :entrée: Dungeon self, int x, int y
        :sortie: EntityType
        :description: Renvoie la valeur de la case (x,y) du donjon.
        '''
        return self.grid[y][x]
    
    def get_total_construction_cost(self):
        '''
        :entrée: Dungeon self
        :sortie: int
        :description: Calcule et renvoie le coût total actuel du donjon.
        '''
        total = 0
        # Coût des murs 
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == EntityType.WALL:
                    total += COSTS[EntityType.WALL]
    
        # Coût des pièges 
        for trap_obj in self.trap.values():
            total += trap_obj.cost
        return total 

    def get_trap(self, x, y):
        '''
        :entrée: Dungeon self, int x, int y
        :sortie: Trap
        :description: Renvoie le piège placé aux coordonnées (x,y).
        '''
        return self.trap.get((x, y))

    def get_monster(self, x, y):
        '''
        :entrée: Dungeon self, int x, int y
        :sortie: Monster
        :description: Renvoie le monstre placé aux coordonnées (x,y).
        '''
        return self.monsters.get((x, y))
    
    def to_dict(self):
        '''
        :entrée: Dungeon self
        :sortie: dict<String>
        :description: Renvoie un dictionnaire : {"width" : int largeur du donjon, 
                                                "height" : int hauteur du donjon, 
                                                "entry_pos" : tuple<int> position de l'entrée, 
                                                "treasure_pos : tuple<int> position de l'entrée,
                                                "walls" : list<tuple<int>> liste des positions des murs du donjon,
                                                "traps": list<tuple<String>> list des classes et niveau des pièges du donjon,
                                                "monsters" : list<tuple<int>> liste des coordonnées de smonstres du donjon }
        '''
        traps_data = {} #dictionnaire detaillé pour les traps
        for pos, trap_obj in self.trap.items():
            traps_data[f"{pos[0]},{pos[1]}"] = {
                "class": trap_obj.__class__.__name__,
                "level": trap_obj.level
            }

        return {
            "width": self.width,
            "height": self.height,
            "entry_pos": self.entry_pos,
            "treasure_pos": self.treasure_pos,
            "walls": [(x, y) for y in range(self.height) for x in range(self.width) 
                      if self.grid[y][x] == EntityType.WALL],
            "traps": traps_data, 
            "monsters": [(x, y) for y in range(self.height) for x in range(self.width) 
                         if self.grid[y][x] == EntityType.MONSTER]
        }


    
    @classmethod
    def from_dict(cls, data):
        '''
        :entrée: cls (equvalent de 'self' pour les classes), data (dict<string> contenant les données d'une map ou d'une partie)
        :sortie: dungeon
        :descritpion: a partir d'un dictionnaire de données om_dict elle va créer un dungeon
        '''
        d = cls(data.get("width", 32), data.get("height", 32))
        d.entry_pos = tuple(data.get("entry_pos", (0, 0)))
        d.treasure_pos = tuple(data.get("treasure_pos", (d.width-1, d.height-1)))

        # Restauration des murs
        for x, y in data.get("walls", []):
            d.grid[y][x] = EntityType.WALL

        # Restauration des monstres
        for x, y in data.get("monsters", []):
            d.grid[y][x] = EntityType.MONSTER
            # On recrée l'objet Monster pour qu'il soit interactif
            # Note: On utilise des valeurs par défaut si elles ne sont pas dans la map
            new_monster = Monster(
                id=len(d.monsters), 
                hp=50, 
                damage=10, 
                start_pos=(x, y), 
                cost=40
            )
            d.monsters[(x, y)] = new_monster

        # classes de pièges
        trap_classes = {
            "Spike": Spike,
            "Hole": Hole,
            "Fire": Fire,
            "Rune": Rune
        }

        # Restauration des pièges détaillés
        traps_info = data.get("traps", {})
        if isinstance(traps_info, dict):
            for pos_str, info in traps_info.items():
                x, y = map(int, pos_str.split(","))
                trap_class = trap_classes.get(info["class"], Spike)
                d.grid[y][x] = EntityType.TRAP
                d.trap[(x, y)] = trap_class(level=info.get("level", 1))
        else:
            # Compatibilité avec les anciennes sauvegardes
            for x, y in traps_info:
                d.grid[y][x] = EntityType.TRAP
                d.trap[(x, y)] = Spike() # Défaut

        return d


        

    def there_is_a_way(self, x, y, cible_x, cible_y, already_visited: list):
        '''
        :entrée: Dungeon self, int x, int y, int cible_x, int cible_y, list<tuple<int>> already_visited
        :sortie: bool
        :descrition: Renvoie si il existe toujours un chemin possible entre (x,y) et (cible_x, cible_y)
        '''
        # Cas de réussite
        if x == cible_x and y == cible_y:
            return True
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in directions:
            next_x = x + d[0]
            next_y = y + d[1]
            next_pos = (next_x, next_y)
            
            if next_pos not in already_visited:
                if self.is_valid_pos(next_x, next_y) and self.grid[next_y][next_x] != EntityType.WALL:
                    already_visited.append(next_pos)
                    if self.there_is_a_way(next_x, next_y, cible_x, cible_y, already_visited):
                        return True
        # Cas d'échec (pas de chemin depuis cette case)
        return False