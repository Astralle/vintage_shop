import os, json
from flask import Flask, render_template, jsonify

# Tell Flask to look for templates in public/html
# and serve static files from public/static
app = Flask(
    __name__,
    template_folder="public/html",
    static_folder="public/static",
    static_url_path="/static"
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(fname):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---- Page routes ----
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/boutique")
def boutique():
    return render_template("boutique.html")

@app.route("/product/<int:id>")
def product(id):
    products = load_json("products.json")
    item = next((p for p in products if p["id"] == id), None)
    return render_template("product.html", product=item)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/mentions")
def mentions():
    return render_template("mentions-legales.html")

# ---- JSON API ----
@app.route("/api/products")
def api_products():
    return jsonify(load_json("products.json"))

@app.route("/api/featured")
def api_featured():
    return jsonify(load_json("featured.json"))

if __name__ == "__main__":
    app.run(debug=True)
