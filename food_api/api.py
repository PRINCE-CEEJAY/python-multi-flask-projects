from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS


api = Flask(__name__)
api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food.db"
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(api)
CORS(api, methods = ["GET", "POST", "PUT", "PATCH"]) 
from flask_cors import CORS


api = Flask(__name__)
api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food.db"
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(api)
CORS(api, methods = ["GET", "POST", "UPDATE"])
CORS(api, methods=["GET", "POST", "PUT", "PATCH"]) 
# Browsers can only do safe operations here
# Delete is admin-controlled inside backend logic


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "price": self.price
        }

# ROUTES
@api.route("/")
def index():
    return render_template("index.html")

@api.route("/foods", methods=["GET"])
def get_foods():
    menu = Food.query.all()
    if menu:
        return jsonify({"data": [food.to_dict() for food in menu]}), 200
    else:
        return jsonify({"message": "No food available"}), 404
    
@api.route("/foods/<int:id>", methods=["GET"])
def get_food(id):
    food = db.session.get(Food, id)
    if not food:
        return jsonify({"message": "no food with the supplied id in the database"}), 404
    else:
        return jsonify(food.to_dict()), 200

@api.route("/foods", methods=["POST"])
def add_food():
    data = request.get_json()
    category = data.get("category")
    title = data.get("title")
    price = int(data.get("price"))

    if not category or not title or not price:
        return jsonify({"message":"No empty field allowed"}), 404
    else:
        new_food = Food(category=category, title=title, price=price)
        try:
            db.session.add(new_food)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"message":"Food title already exists"}), 404
        return jsonify({"message":"Added successfully", "data": new_food.to_dict()}), 200


@api.route("/foods/<int:id>", methods=["PUT"])
def update_food(id):    
    data = request.get_json()
    food_category = data.get("category")
    food_title = data.get("title")
    food_price = int(data.get("price"))

    food = db.session.get(Food, id)
    if not food:
        return jsonify({"message":"sorry, the requested food does not exist in the database"}), 404
    else:
        food.category = food_category
        food.title = food_title
        food.price = food_price
        db.session.commit()
        return jsonify({"message":"successfully updated"}), 200

@api.route("/foods/<int:id>", methods=["DELETE"])
def delete_food(id):
    food = db.session.get(Food, id)
    if not food:
        return jsonify({"message":"no food with the supplied id in the database"}), 404
    else:
        db.session.delete(food)
        db.session.commit()
        return jsonify({"message":"food deleted successfully"}), 200
      
    
if __name__ == "__main__":
    with api.app_context():
        db.create_all()
    api.run(debug=True)