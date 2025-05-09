import os, json, time
from flask import Flask, jsonify, request, send_from_directory, abort

# ─── Paths ────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
DATA_FILE  = os.path.join(BASE_DIR, 'data', 'featured.json')

app = Flask(
    __name__,
    static_folder=PUBLIC_DIR,   # serves /style.css, /script.js, etc
    static_url_path=''          # at the app root
)

# ─── Helpers ───────────────────────────────────────────────────────────────
def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── Frontend routes ──────────────────────────────────────────────────────
@app.route('/')
def index():
    # Serve exactly public/index.html
    return send_from_directory(PUBLIC_DIR, 'index.html')

@app.errorhandler(404)
def spa_fallback(e):
    # If it’s an API call, give the 404 back
    if request.path.startswith('/api/'):
        return e
    # Otherwise assume it's a client-side route and serve index.html
    return send_from_directory(PUBLIC_DIR, 'index.html')

# ─── API routes ────────────────────────────────────────────────────────────
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        return jsonify(read_data())
    except:
        abort(500, description="Unable to read data")

@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.get_json(force=True)
    if not isinstance(new_item, dict):
        abort(400, "Invalid JSON body")
    items = read_data()
    new_item['id'] = int(time.time() * 1000)
    items.append(new_item)
    write_data(items)
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated = request.get_json(force=True)
    if not isinstance(updated, dict):
        abort(400, "Invalid JSON body")
    items = read_data()
    for idx, itm in enumerate(items):
        if itm.get('id') == item_id:
            updated['id'] = item_id
            items[idx] = { **itm, **updated }
            write_data(items)
            return jsonify(items[idx])
    abort(404, "Item not found")

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = read_data()
    new_list = [itm for itm in items if itm.get('id') != item_id]
    if len(new_list) == len(items):
        abort(404, "Item not found")
    write_data(new_list)
    return '', 204

# ─── Run ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
