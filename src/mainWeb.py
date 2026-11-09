
from flask import Flask, render_template, request,jsonify, redirect, url_for
from models.gameState import GameState, cout_th
from models.dungeon import Dungeon
from models.entity import *
from copy import copy
import json
import os


app = Flask(__name__)

SAVE_DIR = "saves"
MAPS_DIR = os.path.join(SAVE_DIR, "maps")
GAMES_DIR = os.path.join(SAVE_DIR, "games")

os.makedirs(MAPS_DIR, exist_ok=True)
os.makedirs(GAMES_DIR, exist_ok=True)

dungeon = None
game = None
grid_width = 0
grid_height = 0
lastWaveActive = False

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/create_game', methods=['POST'])
def create_game():
    global game, dungeon, grid_width, grid_height
    try:
        width = int(request.form.get('width', 10))
        height = int(request.form.get('height', 10))
        
        width = max(5, min(width, 25))
        height = max(5, min(height, 20))
        
        dungeon = Dungeon(width, height)
        game = GameState(dungeon)

        grid_width = width
        grid_height = height

        return redirect(url_for('play_game'))
    except ValueError:
        return redirect(url_for('home'))


@app.route('/game')
def play_game():
    if game is None:
        return redirect(url_for('home'))
    return render_template('index.html')



@app.route('/api/state', methods=['GET'])
def get_state():
    global game, dungeon, lastWaveActive
    if game is None or dungeon is None : 
        return jsonify({"error": "No game"}), 400
    
    w = game.dungeon.width
    h = game.dungeon.height

    # Création de la grille avec murs autour
    grid_data = []
    for y in range(h + 2):
        row = []
        for x in range(w + 2):
            # Cas des bordures extérieures (Murs forcés)
            if y == 0 or y == h + 1 or x == 0 or x == w + 1:
                row.append(EntityType.WALL.value)
            else:
                # Coordonnées réelles dans le donjon (on enlève le décalage de la bordure)
                rx, ry = x - 1, y - 1
                
                cell = game.dungeon.get_cell(rx, ry)
                # On récupère les objets via les dictionnaires du donjon
                element = game.dungeon.trap.get((rx, ry))
                monster = game.dungeon.monsters.get((rx, ry))

                if monster is not None:
                    row.append(20) # Code pour monstre
                elif element is not None:
                    # Logique des pièges
                    if isinstance(element, Hole):
                        if element.level == 1: row.append(10)
                        elif element.level == 2: row.append(11)
                        elif element.level == 3: row.append(12)
                    elif isinstance(element, Spike):
                        row.append(4)
                    elif isinstance(element, Rune):
                        row.append(13)
                    elif isinstance(element, Fire):
                        row.append(14)
                    else:
                        row.append(cell.value)
                else:
                    row.append(cell.value)
        grid_data.append(row)
        
    loaded_heroes = game.get_loaded_heros()
    # décaler la position des héros aussi
    heroes = []
    for h in loaded_heroes:
        if not h.isDead:
            heroes.append({
                "x": h.pos[0] + 1,
                "y": h.pos[1] + 1,
                "hp": h.hp,
                "strategy": h.strategy
            })

    if not game.waveActive and lastWaveActive:
        justFinished = True
    else:
        justFinished = False
    lastWaveActive = game.waveActive

    return jsonify({
        "grid": grid_data,
        "budget": game.budget,
        "waveActive": game.waveActive,
        "wave": game.nbWave, 
        "heroes": [{"x": h.pos[0], "y": h.pos[1], "hp": h.hp, "strategy" : h.strategy, "maxHp" : h.maxHp, "boss" : h.boss} for h in loaded_heroes if not h.isDead],
        "monsters": [{"x": pos[0], "y": pos[1], "hp": m.hp, "maxHp": m.maxHp} for pos, m in game.dungeon.monsters.items()],
        "costs" : {
            "WALL" : COSTS[EntityType.WALL],
            "PIC" : Spike.get_cost(game.levels[Spike]),
            "HOLE" : Hole.get_cost(game.levels[Hole]),
            "RUNE" : Rune.get_cost(),
            "FIRE" : Fire.get_cost(),
            "MONSTER" : COSTS[EntityType.MONSTER]},
        "upgrade_costs" : {
            "PIC" : Spike.get_upgrade_cost(game.levels[Spike]),
            "HOLE" : Hole.get_upgrade_cost(game.levels[Hole])
        },
        "score" : game.score,
        "justFinished" : justFinished
    })

@app.route('/api/place', methods=['POST'])
def place_element():
    if game is None or dungeon is None:
        return jsonify({"error": "No game"}), 400
    
    data = request.json
    x, y = data['x'], data['y']

    # IMPORTANT : on enlève 1 pour compenser la bordure
    x -= 1
    y -= 1

    # on vérifie que x,y sont toujours valides
    if x < 0 or y < 0 or x >= game.dungeon.width or y >= game.dungeon.height:
        return jsonify({"success": False, "budget": game.budget, "message": "Position hors limites"}), 400

    element_str = data['type']

    element = None
    target_type = EntityType.EMPTY
    if element_str == "WALL":
        target_type = EntityType.WALL
    elif element_str == "PIC":
        target_type = EntityType.TRAP
        element = Spike(level=game.levels[Spike])
    
    elif element_str == "HOLE":
        target_type = EntityType.TRAP
        element = Hole(level=game.levels[Hole])

    elif element_str == "RUNE" :
        target_type = EntityType.TRAP
        element = Rune()
    elif element_str == "FIRE" :
        target_type = EntityType.TRAP
        element = Fire()

    elif element_str == "MONSTER":
        target_type = EntityType.MONSTER
        element = Monster(len(game.dungeon.monsters), 60, 20, (x,y), 40)

    elif element_str == "EMPTY": target_type = EntityType.EMPTY
    
    success = game.buyElement(x, y, target_type, copy(element))
    return jsonify({"success": success, "budget": game.budget})


@app.route('/api/upgrade', methods=['POST'])
def upgrade_trap():
    if game is None or dungeon is None : return jsonify({"error": "No game"}), 400
    data = request.json
    trap = data["trap"]

    success = False
    if trap == "HOLE":
        success = game.upgradeTrap(Hole)
    elif trap == "PIC":
        success = game.upgradeTrap(Spike)
    
    return jsonify({"success": success, "budget": game.budget})




@app.route('/api/wave/start', methods=['POST'])
def start_wave():
    if game is None or dungeon is None : return jsonify({"error": "No game"}), 400
    game.startWave()
    return jsonify({"status": "started"})

@app.route('/api/wave/update', methods=['POST'])
def update_wave():
    if game is None or dungeon is None : return jsonify({"error": "No game"}), 400
    res = game.updateWave()
    if res:
        res = list(res)
        res.append(game.nbWave)
    return jsonify({"status": "updated", "updateNews" : res})

@app.route('/api/restart', methods=['POST'])
def restart_game():
    global game, dungeon, grid_width, grid_height
    # recrée un donjon vierge, même taille que celui initial
    dungeon = Dungeon(grid_width, grid_height)
    game.restartGame(grid_width, grid_height)  # reset budget etc.
    return jsonify({"status": "success", "message": "Partie redémarrée"})


@app.route('/api/saves', methods=['GET'])
def list_saves():
    maps = [f for f in os.listdir(MAPS_DIR) if f.endswith('.json')]
    games = [f for f in os.listdir(GAMES_DIR) if f.endswith('.json')]
    return jsonify({"maps": maps, "games": games})


@app.route('/api/map_info/<filename>', methods=['GET'])
def get_map_info(filename):
    # Route pour récupérer les infos avant de charger
    filepath = os.path.join(MAPS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    with open(filepath, "r") as f:
        data = json.load(f)
    
    # On calcule le coût théorique par rapport au donjon actuel
    temp_dungeon = Dungeon.from_dict(data.get("dungeon",data)) 
    if temp_dungeon.width != game.dungeon.width or temp_dungeon.height != game.dungeon.height:
        return jsonify({
            "width": temp_dungeon.width,
            "height": temp_dungeon.height,
            "cost": "Incompatible",
            "error": "Taille différente"
        })

    cost = cout_th(game.dungeon, temp_dungeon)
    
    return jsonify({
        "width": temp_dungeon.width,
        "height": temp_dungeon.height,
        "cost": cost
    })

@app.route('/api/save_map', methods=['POST'])
def save_map():    #rajouter le cout de la map et le soustraire au nb or
    if game is None or dungeon is None : return jsonify({"error": "No game"}), 400

    #Sauvegarde uniquement la structure map
    data = request.json
    name = data.get('name', 'map_layout')
    filename = os.path.join(MAPS_DIR, f"{name}.json")
    game.saveMap_to_file(filename) 
    return jsonify({"status": "success", "message": "Map sauvegardée"})

@app.route('/api/save_game', methods=['POST'])
def save_game():
    """Sauvegarde l'état complet de la partie (Map + Score + Budget)"""
    if game is None or dungeon is None : return jsonify({"error": "No game"}), 400

    data = request.json
    name = data.get('name', 'game_session')
    filename = os.path.join(GAMES_DIR, f"{name}.json")
    game.saveGame_to_file(filename) 
    return jsonify({"status": "success", "message": "Partie sauvegardée"})

@app.route('/api/load', methods=['POST'])
def load_save():
    if game is None or dungeon is None : return jsonify({"error": "No game"}), 400
    data=request.json
    filename = data.get('filename')
    save_type = data.get('type') # 'map' ou 'game'
    
    if save_type == 'map':
        full_path = os.path.join(SAVE_DIR, "maps", filename)
        print(f"Tentative de chargement : {full_path}")

        try:
            if os.path.exists(full_path):
                # On charge les données pour vérifier la taille avant
                with open(full_path, "r") as f:
                    content = json.load(f)

                dungeon_data = content.get("dungeon", content)

                if dungeon_data.get("width") != game.dungeon.width or dungeon_data.get("height") != game.dungeon.height:
                    return jsonify({
                        "status": "error", 
                        "message": f"Dimensions incompatibles ! (Map chargée: {dungeon_data.get('width')}x{dungeon_data.get('height')}, Map actuelle: {game.dungeon.width}x{game.dungeon.height})"
                    }), 400

                if game.load_from_file(full_path): # Si la taille est bonne on lance le chargement
                    return jsonify({"status": "success", "message": "Chargement réussi", "budget": game.budget})

            return jsonify({"status": "error", "message": "Fichier introuvable"}), 500

        except ValueError as e:
            # On renvoie le message d'erreur du GameState
            return jsonify({"status": "error", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": "Erreur serveur : " + str(e)}), 500

    else:
        full_path = os.path.join(SAVE_DIR, "games", filename)
        print(f"Tentative de chargement : {full_path}")
        try:
            if game.load_from_file(full_path):
                return jsonify({"status": "success","message": "Chargement réussi","budget": game.budget})
            else:
                return jsonify({"status": "error", "message": "Échec du chargement"}), 400
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    

if __name__ == "__main__":
    app.run(debug=True)