from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
# from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# CORS(app, origins = ["http://localhost:5173"])

db = SQLAlchemy(app)

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
            "image": self.image,
            "quantity": self.quantity,
        }
        
def add():
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    category = data.get("category")
    image = data.get("image")
    quantity = data.get("quantity")

    items = [name, price, category, image, quantity]
    if any(item is None or item == "" for item in items):
        return jsonify({"status": "all fields are required"})
    
    new_product = ProductModel(name=name, price=int(price), category=category, image=image, quantity=int(quantity))

    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"data": new_product.to_dict()})
    except IntegrityError:  #product already exist
        db.session.rollback()
        return jsonify({"status":"product already exist"})
    

def get_all():
    all_products = ProductModel.query.all()
    if all_products:
        formattedd = [product.to_dict() for product in all_products]
        return jsonify({"data": formattedd})
    else:
        return jsonify({"status":"No product available"})


def get_one(id):
    product = db.session.get(ProductModel, id)
    if product:
        return jsonify({"data": product.to_dict()})
    else:
        return jsonify({"status":"Product does not exist"})

def update(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"status": "product doesn't exist"})
    else:
        data = request.get_json()
        name = data.get("name", product.name)
        price = data.get("price", product.price)
        category = data.get("category", product.category)
        image = data.get("image", product.image)
        quantity = data.get("quantity", product.quantity)

        product.name = name
        product.price = int(price)
        product.category = category
        product.image = image
        product.quantity = int(quantity)

        db.session.commit()

        return jsonify({"status": "product updated successfully", "data": product.to_dict()})
            

def delete(id):
    product = ProductModel.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"status":"product deleted"})
    else:
        return jsonify({"status":"product does not exist"})
    
#  ROUTES 
@app.route("/")
def home():
    return jsonify({"status":"Server is running ..."})

@app.route("/products", methods = ["GET"])
def get_products():
   return get_all()

@app.route("/products", methods = ["POST"])
def add_products():
    return add()

@app.route("/products/<int:id>", methods = ["GET"])
def get_product(id):
    return get_one(id)

@app.route("/products/<int:id>", methods = ["PUT"])
def update_product(id):
    return update(id)

@app.route("/products/<int:id>", methods = ["DELETE"])
def delete_product(id):
    return delete(id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)