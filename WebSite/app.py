import os
import json
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    abort,
    redirect,
    url_for,
    session
)
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename

# ---- Config ----
app = Flask(
    __name__,
    template_folder="public/html",
    static_folder="public/static",
    static_url_path="/static"
)

# Secret key for session cookies (make this unpredictable in production)
app.secret_key = "y6;qLb4Z#=({jED?YV^uPt"

# Hard-coded admin password
ADMIN_PASSWORD = "4home1952"

# Data & images directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMAGES_DIR = os.path.join(app.static_folder, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"png"}


def load_json(fname):
    with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(fname, data):
    with open(os.path.join(DATA_DIR, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---- Authentication routes ----

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == ADMIN_PASSWORD:
            session["admin_authenticated"] = True
            return redirect(url_for("admin"))
        else:
            error = "Mot de passe incorrect"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("admin_authenticated", None)
    return redirect(url_for("login"))


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


# plan-du-site under endpoint "plan"
@app.route("/plan-du-site", endpoint="plan")
def plan_du_site():
    return render_template("plan-du-site.html")


# mentions-legales under endpoint "mentions"
@app.route("/mentions-legales", endpoint="mentions")
def mentions_legales():
    return render_template("mentions-legales.html")


@app.route("/cookies")
def cookies():
    return render_template("cookies.html")


@app.route("/politique")
def politique():
    return render_template("politique.html")


# ---- Admin page (protected) ----

@app.route("/admin")
def admin():
    if not session.get("admin_authenticated"):
        return redirect(url_for("login"))
    return render_template("admin.html")


# ---- Catch-all for *.html (protect admin.html) ----

@app.route("/<page>.html")
def html_pages(page):
    if page == "admin":
        return redirect(url_for("login"))
    try:
        return render_template(f"{page}.html")
    except TemplateNotFound:
        abort(404)


# ---- Products JSON API ----

@app.route("/api/products", methods=["GET"])
def api_products():
    return jsonify(load_json("products.json"))


@app.route("/api/products", methods=["POST"])
def create_product():
    if not session.get("admin_authenticated"):
        return jsonify({"error": "Unauthorized"}), 401

    form = request.form
    name = form["name"].strip()
    price = form["price"].strip()
    short_desc = form["short-description"].strip()
    long_desc = form["long-description"].strip()
    tags = [t.strip() for t in form.get("tags", "").split(",") if t.strip()]

    products = load_json("products.json")
    next_id = max((p.get("id", 0) for p in products), default=0) + 1

    prod = {
        "id": next_id,
        "name": name,
        "price": price,
        "shortDescription": short_desc,
        "longDescription": long_desc,
        "tags": tags,
        "coverImage": None,
        "detailImages": []
    }

    # Handle cover image
    cover = request.files.get("cover")
    if cover and allowed_file(cover.filename):
        filename = f"img_{next_id}_cover.png"
        cover.save(os.path.join(IMAGES_DIR, filename))
        prod["coverImage"] = f"images/{filename}"

    # Handle detail images
    for idx, file in enumerate(request.files.getlist("details")[:3], start=1):
        if file and allowed_file(file.filename):
            fn = f"img_{next_id}_detail_{idx}.png"
            file.save(os.path.join(IMAGES_DIR, fn))
            prod["detailImages"].append(f"images/{fn}")

    products.append(prod)
    save_json("products.json", products)
    return jsonify(prod), 201


@app.route("/api/products/<int:id>", methods=["GET"])
def get_product(id):
    products = load_json("products.json")
    prod = next((p for p in products if p["id"] == id), None)
    if not prod:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(prod)


@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    if not session.get("admin_authenticated"):
        return jsonify({"error": "Unauthorized"}), 401

    products = load_json("products.json")
    prod = next((p for p in products if p["id"] == id), None)
    if not prod:
        return jsonify({"error": "Product not found"}), 404

    form = request.form
    # Update text fields
    for fld, key in [
        ("name", "name"),
        ("price", "price"),
        ("short-description", "shortDescription"),
        ("long-description", "longDescription"),
        ("tags", "tags")
    ]:
        val = form.get(fld)
        if val is not None:
            prod[key] = [t.strip() for t in val.split(",")] if fld == "tags" else val.strip()

    # Replace cover image
    cover = request.files.get("cover")
    if cover and allowed_file(cover.filename):
        if prod.get("coverImage"):
            try:
                os.remove(os.path.join(app.static_folder, prod["coverImage"]))
            except:
                pass
        fn = f"img_{id}_cover.png"
        cover.save(os.path.join(IMAGES_DIR, fn))
        prod["coverImage"] = f"images/{fn}"

    # Replace detail images
    details = request.files.getlist("details")
    if details:
        for old in prod.get("detailImages", []):
            try:
                os.remove(os.path.join(app.static_folder, old))
            except:
                pass
        prod["detailImages"] = []
        for idx, file in enumerate(details[:3], start=1):
            if file and allowed_file(file.filename):
                fn = f"img_{id}_detail_{idx}.png"
                file.save(os.path.join(IMAGES_DIR, fn))
                prod["detailImages"].append(f"images/{fn}")

    save_json("products.json", products)
    return jsonify(prod)


@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    if not session.get("admin_authenticated"):
        return jsonify({"error": "Unauthorized"}), 401

    products = load_json("products.json")
    prod = next((p for p in products if p["id"] == id), None)
    if not prod:
        return jsonify({"error": "Product not found"}), 404

    # Delete images
    if prod.get("coverImage"):
        try:
            os.remove(os.path.join(app.static_folder, prod["coverImage"]))
        except:
            pass
    for img in prod.get("detailImages", []):
        try:
            os.remove(os.path.join(app.static_folder, img))
        except:
            pass

    products.remove(prod)
    save_json("products.json", products)
    return "", 204


# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True)
