import os, json, time
from flask import Flask, jsonify, request, send_from_directory, abort, Response

# ─── Config ───────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
DATA_FILE  = os.path.join(BASE_DIR, 'data', 'featured.json')

# Your fixed, strong key. Change this to something long & random.
# (You could also load from an environment variable if you prefer.)
API_KEY = 'C8f7#tYp9!Lq3@XzW4^Vb0&amp;R7eN2$Mn'

app = Flask(__name__,
            static_folder=PUBLIC_DIR,
            static_url_path='')

# ─── Helpers ───────────────────────────────────────────────────────────────
def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def require_key():
    key = request.headers.get('X-API-KEY')
    if key != API_KEY:
        return Response('{"error":"Unauthorized"}', 401, {'Content-Type':'application/json',
                                                         'WWW-Authenticate':'API key required'})
    return None

# ─── Front-end routes ─────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(PUBLIC_DIR, 'index_inv.html')

@app.errorhandler(404)
def spa_fallback(e):
    if request.path.startswith('/api/'):
        return e
    return send_from_directory(PUBLIC_DIR, 'index_inv.html')

# ─── API: Read is open ─────────────────────────────────────────────────────
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        return jsonify(read_data())
    except:
        abort(500, description="Unable to read data")

# ─── API: Writes require the key ────────────────────────────────────────────
@app.route('/api/items', methods=['POST'])
def add_item():
    if err := require_key(): return err

    new_item = request.get_json(force=True)
    if not isinstance(new_item, dict):
        abort(400, "Invalid JSON")
    items = read_data()
    new_item['id'] = int(time.time() * 1000)
    items.append(new_item)
    write_data(items)
    return jsonify(new_item), 201

@app.route('/api/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    if err := require_key(): return err

    try:
        item_id = int(item_id)
    except ValueError:
        abort(400, "Invalid item id")

    updated = request.get_json(force=True)
    if not isinstance(updated, dict):
        abort(400, "Invalid JSON")
    items = read_data()
    for i, itm in enumerate(items):
        if itm.get('id') == item_id:
            updated['id'] = item_id
            items[i] = { **itm, **updated }
            write_data(items)
            return jsonify(items[i])
    abort(404, "Item not found")

@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    if err := require_key(): return err

    try:
        item_id = int(item_id)
    except ValueError:
        abort(400, "Invalid item id")
    items = read_data()
    new_list = [itm for itm in items if itm.get('id') != item_id]
    if len(new_list) == len(items):
        abort(404, "Item not found")
    write_data(new_list)
    return '', 204

# ─── Run ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
