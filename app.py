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
from datetime import datetime

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
ADMIN_PASSWORD = "4home1952-@zDX()&@"

# Data & images directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMAGES_DIR = os.path.join(app.static_folder, "images")
# Ensure directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff", "svg"}


def load_json(fname):
    with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(fname, data):
    with open(os.path.join(DATA_DIR, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---- Authentication routes ----

@app.route("/dx&HY@aa", methods=["GET", "POST"])
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


# Contact route: handles JSON POST and writes to contacts.json
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        # Ensure client timestamp, fallback to server
        data.setdefault('timestamp', datetime.now().isoformat())

        # Load existing contacts
        contacts = load_json("contacts.json")
        # Append and save
        contacts.append(data)
        save_json("contacts.json", contacts)
        return jsonify({"status": "success"}), 200

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

@app.route("/reservation")
def reservation():
    return render_template("reservation.html")

# ---- Admin page (protected) ----
@app.route("/dx&HY@aa-True")
def admin():
    if not session.get("admin_authenticated"):
        return redirect(url_for("login"))
    return render_template("admin.html")

# ---- Catch-all for *.html ----
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

    cover = request.files.get("cover")
    if cover and allowed_file(cover.filename):
        ext = cover.filename.rsplit(".", 1)[1].lower()
        filename = f"img_{next_id}_cover.{ext}"
        cover.save(os.path.join(IMAGES_DIR, filename))
        prod["coverImage"] = f"images/{filename}"

    for idx, file in enumerate(request.files.getlist("details")[:3], start=1):
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            fn = f"img_{next_id}_detail_{idx}.{ext}"
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

@app.route("/api/reservations", methods=["POST"])
def create_reservation():
    data = request.get_json() or {}
    fname = data.get("first_name", "").strip()
    lname = data.get("last_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    pickup_date = data.get("pickup_date", "").strip()
    pickup_time = data.get("pickup_time", "").strip()
    product_id = data.get("product_id")
    product_name = data.get("product_name", "")
    price = data.get("price")

    pickup_datetime = f"{pickup_date}T{pickup_time}"
    reservation_datetime = datetime.now().isoformat()

    obj = {"id": product_id, "name": product_name, "price": price}

    reservations = load_json("reservation.json")

    reservation = {
        "name": f"{lname} {fname}",
        "email": email,
        "phone": phone,
        "pickup_datetime": pickup_datetime,
        "reservation_datetime": reservation_datetime,
        "price": price,
        "objects": [obj]
    }
    reservations.append(reservation)
    save_json("reservation.json", reservations)

    return jsonify({"status": "success"}), 201

@app.route("/api/reservations", methods=["GET"])
def list_reservations():
    reservations = load_json("reservation.json")
    for idx, r in enumerate(reservations):
        r["_idx"] = idx
    return jsonify(reservations)

@app.route("/api/reservations/<int:idx>", methods=["DELETE"])
def delete_reservation(idx):
    reservations = load_json("reservation.json")
    if idx < 0 or idx >= len(reservations):
        abort(404, "Reservation not found")
    reservations.pop(idx)
    save_json("reservation.json", reservations)
    return "", 204

@app.route("/api/contacts/<int:idx>", methods=["DELETE"])
def delete_contact(idx):
    """Delete the contact message at index `idx`."""
    contacts = load_json("contacts.json")
    if idx < 0 or idx >= len(contacts):
        abort(404, "Contact not found")
    contacts.pop(idx)
    save_json("contacts.json", contacts)
    return "", 204


# ---- Contacts JSON API ----
@app.route("/api/contacts", methods=["GET"])
def list_contacts():
    """Return the full array of contact messages."""
    contacts = load_json("contacts.json")
    for idx, m in enumerate(contacts):
        m["_idx"] = idx
    return jsonify(contacts)

# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True)
