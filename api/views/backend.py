# api/index.py
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- TEMPORARY IN-MEMORY "DATABASE" ---
# This will be wiped clean after every request on Vercel.
GAME_STATE = {
    'tiles': [],
    'picksMade': 0,
    'selections': [],
    'revealed': False
}

def initialize_game(num_participants=20):
    global GAME_STATE
    
    # We need 20 tiles in total, but only 17 will have numbers
    num_pickable_tiles = num_participants - 3
    
    # We create a list of numbers from 4 to 20 to ensure 1, 2, and 3 are never used
    numbers = list(range(4, num_pickable_tiles + 4))
    random.shuffle(numbers)
    
    tiles = []
    
    # We create 17 pickable tiles with numbers
    for i in range(num_pickable_tiles):
        tiles.append({'id': i, 'number': numbers[i], 'pickedBy': None})
        
    # We create 3 empty, un-pickable tiles
    for i in range(3):
        tiles.append({'id': num_pickable_tiles + i, 'number': 'Empty', 'pickedBy': 'Empty'})
        
    random.shuffle(tiles) # Shuffle all tiles to mix the empty ones in
    
    GAME_STATE = {
        'tiles': tiles,
        'picksMade': 0,
        'selections': [],
        'revealed': False
    }

initialize_game()


# --- API Endpoints ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/game_state', methods=['GET'])
def get_game_state():
    return jsonify(GAME_STATE)

@app.route('/api/pick_tile', methods=['POST'])
def pick_tile():
    data = request.json
    name = data.get('name')
    tile_id = data.get('tileId')
    
    if not name or not tile_id:
        return jsonify({"success": False, "message": "Name and Tile ID are required."})
    
    tile_id = int(tile_id)
    
    # We check if the tile is already picked OR if it's one of the empty ones
    if (tile_id >= len(GAME_STATE['tiles']) or 
        GAME_STATE['tiles'][tile_id]['pickedBy'] is not None):
        return jsonify({"success": False, "message": "This tile has already been picked."})

    GAME_STATE['tiles'][tile_id]['pickedBy'] = name
    GAME_STATE['picksMade'] += 1
    
    GAME_STATE['selections'].append({
        'name': name,
        'number': GAME_STATE['tiles'][tile_id]['number'],
        'tileId': tile_id
    })
    
    return jsonify({"success": True})

@app.route('/api/reveal', methods=['POST'])
def reveal_numbers():
    global GAME_STATE
    # The number of required picks is now 17, not 20
    if GAME_STATE['picksMade'] == 17:
        GAME_STATE['revealed'] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Not all tiles have been picked yet."})
        
@app.route('/api/reset', methods=['POST'])
def reset_game():
    initialize_game()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)