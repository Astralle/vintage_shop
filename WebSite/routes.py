import os, json
from flask import render_template, jsonify

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(fname):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def register_routes(app):
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

