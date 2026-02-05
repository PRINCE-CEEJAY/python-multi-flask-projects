from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

auth = Flask(__name__)

auth.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
auth.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(auth)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email
        }

@auth.route("/")
def index():
    return render_template("index.html") 

@auth.route("/login", methods = ["POST"])
def login():
    data = request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return "you must fill your details into the fields"

    user_email = db.session.get(UserModel, email)

    if user_email:
        stored_password = db.session.get(UserModel, password)     
        
        if password == check_password_hash(stored_password):            
            return render_template("dashboard.html", user = user_email)
    else:
       return render_template("not_found.html")

# user login screen
@auth.route("/login_screen")
def login_screen():
    return render_template("login_screen.html")

@auth.route("/registration_screen")
def registration_screen():
    return render_template("registration.html")

# where user submits registration to
@auth.route("/register", methods = ["POST"])
def register():
    data = request.form

    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")

    if not fullname or not email or not password:
        return jsonify({"No detail supplied"})

    hashed_password = generate_password_hash(password)
    new_user = UserModel(fullname=fullname, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return render_template("dashboard.html", user = fullname)
    except IntegrityError:
        db.session.rollback()
        return redirect(url_for('login_screen'))
    
@auth.route("/admin")
def admin():
    registered_users = [user.to_dict() for user in UserModel.query.all()] 
    # return render_template("admin.html", registered_users=registered_users)
    return jsonify({"users": registered_users})
   
     

if __name__ == "__main__":
    with auth.app_context():
        db.create_all()
    auth.run(debug=True)
