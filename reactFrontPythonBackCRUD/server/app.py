from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid

# -------------------- APP SETUP --------------------

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app, origins=["http://localhost:5173"])

db = SQLAlchemy(app)

# -------------------- MODEL --------------------

class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "image": f"http://localhost:5000/{self.image}",
            "quantity": self.quantity,
        }

# -------------------- HELPERS --------------------

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "ico", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_file):
    filename = secure_filename(image_file.filename)

    if not allowed_file(filename):
        return None

    unique_name = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)

    image_file.save(file_path)

    return file_path

# -------------------- CRUD LOGIC --------------------

# CREATE PRODUCT
def add():
    name = request.form.get("name")
    price = request.form.get("price")
    category = request.form.get("category")
    quantity = request.form.get("quantity")
    image_file = request.files.get("image")

    if not all([name, price, category, quantity, image_file]):
        return jsonify({"status": "all fields are required"}), 400

    image_path = save_image(image_file)

    if not image_path:
        return jsonify({"status": "invalid image type"}), 400

    new_product = ProductModel(
        name=name,
        price=int(price),
        category=category,
        image=image_path,
        quantity=int(quantity)
    )

    try:
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"data": new_product.to_dict()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "product already exists"}), 400


# GET ALL PRODUCTS
def get_all():
    products = ProductModel.query.all()
    return jsonify({"data": [p.to_dict() for p in products]})


# GET SINGLE PRODUCT
def get_one(id):
    product = db.session.get(ProductModel, id)

    if not product:
        return jsonify({"status": "product not found"}), 404

    return jsonify({"data": product.to_dict()})


# UPDATE PRODUCT
def update(id):
    product = db.session.get(ProductModel, id)

    if not product:
        return jsonify({"status": "product not found"}), 404

    name = request.form.get("name", product.name)
    price = request.form.get("price", product.price)
    category = request.form.get("category", product.category)
    quantity = request.form.get("quantity", product.quantity)
    image_file = request.files.get("image")

    # Handle image replacement
    if image_file:
        new_image_path = save_image(image_file)

        if not new_image_path:
            return jsonify({"status": "invalid image type"}), 400

        # Delete old image
        if os.path.exists(product.image):
            os.remove(product.image)

        product.image = new_image_path

    product.name = name
    product.price = int(price)
    product.category = category
    product.quantity = int(quantity)

    db.session.commit()

    return jsonify({
        "status": "product updated",
        "data": product.to_dict()
    })


# DELETE PRODUCT
def delete(id):
    product = db.session.get(ProductModel, id)

    if not product:
        return jsonify({"status": "product not found"}), 404

    # Delete image from storage
    if os.path.exists(product.image):
        os.remove(product.image)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"status": "product deleted"})


# -------------------- IMAGE SERVING --------------------

@app.route("/uploads/<filename>")
def serve_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return jsonify({"status": "Server running"})


@app.route("/products", methods=["GET"])
def get_products():
    return get_all()


@app.route("/products", methods=["POST"])
def add_product():
    return add()


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    return get_one(id)


@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    return update(id)


@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    return delete(id)


# -------------------- RUN --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
