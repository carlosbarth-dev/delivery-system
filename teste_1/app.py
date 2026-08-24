import os
import sqlite3
from datetime import datetime
from functools import wraps
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db():
    if "db" not in g:
        if DATABASE_URL:
            import psycopg
            from psycopg.rows import dict_row
            g.db = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        else:
            g.db = sqlite3.connect("delivery.db")
            g.db.row_factory = sqlite3.Row
    return g.db


def query(sql, params=(), one=False):
    db = get_db()
    placeholder_sql = sql.replace("?", "%s") if DATABASE_URL else sql
    cursor = db.cursor()
    cursor.execute(placeholder_sql, params)
    rows = cursor.fetchall() if cursor.description else []
    db.commit()
    cursor.close()
    return (rows[0] if rows else None) if one else rows


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    id_type = "SERIAL PRIMARY KEY" if DATABASE_URL else "INTEGER PRIMARY KEY AUTOINCREMENT"
    query(f"""CREATE TABLE IF NOT EXISTS users (
        id {id_type}, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL, is_admin INTEGER DEFAULT 0
    )""")
    query(f"""CREATE TABLE IF NOT EXISTS products (
        id {id_type}, name TEXT NOT NULL, description TEXT,
        price REAL NOT NULL, image TEXT, active INTEGER DEFAULT 1,
        created_at TEXT
    )""")
    query(f"""CREATE TABLE IF NOT EXISTS orders (
        id {id_type}, user_id INTEGER NOT NULL, total REAL NOT NULL,
        status TEXT DEFAULT 'Novo', address TEXT NOT NULL, created_at TEXT
    )""")
    query(f"""CREATE TABLE IF NOT EXISTS order_items (
        id {id_type}, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL, price REAL NOT NULL, quantity INTEGER NOT NULL
    )""")
    if not query("SELECT id FROM users WHERE email = ?", ("admin@neondelivery.com",), one=True):
        query("INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)",
              ("Administrador", "admin@neondelivery.com", generate_password_hash("admin123"), 1))
    if not query("SELECT id FROM products", one=True):
        products = [
            ("Neon Smash", "Blend artesanal, cheddar e molho da casa.", 29.90),
            ("Cyber Fries", "Batatas crocantes com páprica e cheddar.", 16.90),
            ("Pink Lemonade", "Limonada rosa refrescante.", 10.00),
        ]
        for name, description, price in products:
            query("INSERT INTO products (name, description, price, created_at) VALUES (?, ?, ?, ?)",
                  (name, description, price, datetime.now().isoformat()))


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Entre na sua conta para continuar.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Acesso permitido apenas ao painel administrativo.", "error")
            return redirect(url_for("shop"))
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def cart_data():
    cart = session.get("cart", {})
    return {"cart_count": sum(cart.values())}


@app.route("/")
def home():
    return redirect(url_for("shop" if session.get("user_id") else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = query("SELECT * FROM users WHERE email = ?", (request.form["email"].lower().strip(),), one=True)
        if user and check_password_hash(user["password"], request.form["password"]):
            session.clear()
            session.update(user_id=user["id"], user_name=user["name"], is_admin=bool(user["is_admin"]), cart={})
            return redirect(url_for("shop"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    name, email, password = request.form["name"].strip(), request.form["email"].lower().strip(), request.form["password"]
    if len(name) < 2 or len(password) < 6:
        flash("Informe seu nome e uma senha de pelo menos 6 caracteres.", "error")
        return redirect(url_for("login"))
    if query("SELECT id FROM users WHERE email = ?", (email,), one=True):
        flash("Esse e-mail já está cadastrado.", "error")
        return redirect(url_for("login"))
    query("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, generate_password_hash(password)))
    flash("Conta criada. Agora entre para pedir.", "success")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/loja")
@login_required
def shop():
    products = query("SELECT * FROM products WHERE active = 1 ORDER BY id DESC")
    return render_template("shop.html", products=products)


@app.route("/carrinho/adicionar/<int:product_id>", methods=["POST"])
@login_required
def add_cart(product_id):
    if not query("SELECT id FROM products WHERE id = ? AND active = 1", (product_id,), one=True):
        flash("Produto indisponível.", "error")
        return redirect(url_for("shop"))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    flash("Produto adicionado ao carrinho.", "success")
    return redirect(request.referrer or url_for("shop"))


@app.route("/carrinho")
@login_required
def cart():
    cart_session = session.get("cart", {})
    items, total = [], 0
    for product_id, quantity in cart_session.items():
        product = query("SELECT * FROM products WHERE id = ?", (int(product_id),), one=True)
        if product:
            subtotal = product["price"] * quantity
            items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
    return render_template("cart.html", items=items, total=total)


@app.route("/carrinho/atualizar", methods=["POST"])
@login_required
def update_cart():
    cart = session.get("cart", {})
    for key in list(cart):
        quantity = int(request.form.get(f"quantity_{key}", 0))
        if quantity > 0:
            cart[key] = min(quantity, 99)
        else:
            cart.pop(key)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    address = request.form["address"].strip()
    if not address:
        flash("Informe o endereço de entrega.", "error")
        return redirect(url_for("cart"))
    cart_session = session.get("cart", {})
    if not cart_session:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for("shop"))
    items, total = [], 0
    for product_id, quantity in cart_session.items():
        product = query("SELECT * FROM products WHERE id = ?", (int(product_id),), one=True)
        if product:
            total += product["price"] * quantity
            items.append((product, quantity))
    query("INSERT INTO orders (user_id, total, address, created_at) VALUES (?, ?, ?, ?)",
          (session["user_id"], total, address, datetime.now().isoformat()))
    order = query("SELECT id FROM orders ORDER BY id DESC LIMIT 1", one=True)
    for product, quantity in items:
        query("INSERT INTO order_items (order_id, product_id, product_name, price, quantity) VALUES (?, ?, ?, ?, ?)",
              (order["id"], product["id"], product["name"], product["price"], quantity))
    session["cart"] = {}
    return render_template("success.html", order_id=order["id"])


def save_image(file):
    if not file or not file.filename:
        return None
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Use uma imagem PNG, JPG, JPEG ou WEBP.")
    filename = f"{uuid4().hex}_{secure_filename(file.filename)}"
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return filename


@app.route("/admin")
@login_required
@admin_required
def admin():
    products = query("SELECT * FROM products ORDER BY id DESC")
    orders = query("SELECT orders.*, users.name AS customer FROM orders JOIN users ON users.id = orders.user_id ORDER BY orders.id DESC LIMIT 8")
    return render_template("admin.html", products=products, orders=orders)


@app.route("/admin/produto", methods=["POST"])
@login_required
@admin_required
def create_product():
    try:
        image = save_image(request.files.get("image"))
        query("INSERT INTO products (name, description, price, image, created_at) VALUES (?, ?, ?, ?, ?)",
              (request.form["name"].strip(), request.form["description"].strip(), float(request.form["price"]), image, datetime.now().isoformat()))
        flash("Produto publicado.", "success")
    except (ValueError, TypeError):
        flash("Revise os dados e o formato da imagem.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/produto/<int:product_id>", methods=["POST"])
@login_required
@admin_required
def edit_product(product_id):
    product = query("SELECT * FROM products WHERE id = ?", (product_id,), one=True)
    if not product:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("admin"))
    try:
        image = save_image(request.files.get("image")) or product["image"]
        query("UPDATE products SET name=?, description=?, price=?, image=?, active=? WHERE id=?",
              (request.form["name"].strip(), request.form["description"].strip(), float(request.form["price"]), image, 1 if request.form.get("active") else 0, product_id))
        flash("Produto atualizado.", "success")
    except (ValueError, TypeError):
        flash("Revise os dados e o formato da imagem.", "error")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
