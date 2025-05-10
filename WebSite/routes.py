# WebSite/routes.py
import os, json
from flask import render_template, jsonify, request, redirect, url_for

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(fname):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(fname, data):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def register_routes(app):
    # ---- Catch direct /index.html requests and redirect to "/" ----
    @app.route("/index.html")
    def index_html():
        return redirect( url_for("index") )

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
        return render_template("product.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/plan-du-site")
    def plan_du_site():
        return render_template("plan-du-site.html")

    @app.route("/mentions-legales")
    def mentions_legales():
        return render_template("mentions-legales.html")

    @app.route("/cookies")
    def cookies():
        return render_template("cookies.html")

    @app.route("/politique")
    def politique():
        return render_template("politique.html")


    # ---- Admin page ----
    @app.route("/admin")
    def admin():
        return render_template("admin.html")


    # ---- JSON API ----
    @app.route("/api/products", methods=["GET"])
    def api_products():
        return jsonify(load_json("products.json"))

    @app.route("/api/products", methods=["POST"])
    def create_product():
        new_product = request.get_json()
        products = load_json("products.json")
        products.append(new_product)
        save_json("products.json", products)
        return jsonify(new_product), 201

    @app.route("/api/products/<int:id>", methods=["GET"])
    def get_product(id):
        products = load_json("products.json")
        prod = next((p for p in products if p["id"] == id), None)
        if not prod:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(prod)

    @app.route("/api/products/<int:id>", methods=["PUT"])
    def update_product(id):
        updated = request.get_json()
        products = load_json("products.json")
        prod = next((p for p in products if p["id"] == id), None)
        if not prod:
            return jsonify({"error": "Product not found"}), 404
        prod.update(updated)
        save_json("products.json", products)
        return jsonify(prod)

    @app.route("/api/products/<int:id>", methods=["DELETE"])
    def delete_product(id):
        products = load_json("products.json")
        prod = next((p for p in products if p["id"] == id), None)
        if not prod:
            return jsonify({"error": "Product not found"}), 404
        products.remove(prod)
        save_json("products.json", products)
        return "", 204
