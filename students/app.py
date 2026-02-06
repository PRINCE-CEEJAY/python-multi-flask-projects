from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
    
def get_users():
    users =  UserModel.query.all()
    return [user.to_dict() for user in users]

def get_user(id):
    return UserModel.query.get(id)

def add_user():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm = data.get("confirm")

    # validate user input
    if not username or not email or not password:
        return render_template("status.html", status = "form must be filled")
    
    if password != confirm:
        return render_template("status.html", status = "password do not match")
    
    # hashe and store password
    hashed_p = generate_password_hash(password)    
    new_user = UserModel(username=username, email=email, password=hashed_p)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:  #user already exist in database
        db.session.rollback()
        return render_template("status.html", status = "User already exists")
    
    return render_template("dashboard.html", user = username)

def login_user():
    # get user form details
    data = request.form
    email = data.get("email")
    password = data.get("password")

    user = UserModel.query.filter_by(email=email).first()
   
    if user and check_password_hash(user.password, password):      
        return render_template("dashboard.html", user = user.username)
    else:   
        return render_template("status.html", status = "user not authorized")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        return add_user()
    else:
        return render_template("register.html")


@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        return login_user()
    else:
        return render_template("login.html")
  
@app.route("/admin")
def admin():
    users = get_users()
    return render_template("admin_panel.html", users = users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)