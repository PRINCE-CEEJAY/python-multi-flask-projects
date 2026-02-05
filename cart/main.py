from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)

def get_cursor():
    with sqlite3.connect("cart.db") as con:
        cursor = con.cursor()
        return cursor
    
def create_table():
    cursor = get_cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart ("
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                amount INTEGER NOT NULL
                ")
    ''')

def to_dict(id, item, amount):
    return {
        "id": id,
        "item": item,
        "amount": amount
    }

def add_item():
    item = request.form.get("item")
    amount = request.form.get("amount")

    cursor = get_cursor()
    cursor.execute("INSERT INTO cart (item, amount) VALUES (?, ?)", (item, amount))

    # get id
    cursor.execute("SELECT id FROM cart")
    unique_ids = cursor.fetchall()
    return to_dict(unique_ids, item, amount)

def get_items():
    cursor = get_cursor().execute("SELECT * FROM cart")
    data = cursor.fetchall()
    if data:
        return data, 200
    return "No Items added yet", 404  

def get_item(id):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM cart WHERE id = ?", (id,))
    data = cursor.fetchall()
    if not data:
        return "item does not exist in the database", 404
    return data, 200

def update_item(id, item, price):
    cursor = get_cursor()
    item = request.form.get("item")
    price = request.form.get("price")

    try:
        cursor.execute("UPDATE cart SET id = ?, item = ?, price = ?", (id, item, price))
        return "Succesfully updated", 200
    except Exception as e:
        return f"Error occurred: {e}", 404

def delete_item(id):
    cursor = get_cursor()
    try:
        cursor.execute("DELETE * FROM cart WHERE id = ?", (id,))
        return "Deleted successfully", 200
    except Exception as e:
        return f"Error deleting file /item does not exist {e}", 404
    

# ROUTES
@app.route("/")
def index():
    return render_template("add_item.html")

@app.route("/add_item")
def add_product():    
   return add_item()

@app.route("/get_items")
def get_all():
   return get_items()

@app.route("/get_item/<int:id>")
def get_single_item():
   return get_item(id)

@app.route("/update_item/<int:id>")
def update():
    return update_item(id)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)