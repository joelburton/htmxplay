from flask import Flask, request, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/todos"

CORS(app)
todos = PyMongo(app).db.todos

@app.get("/")
def home():
    return render_template("index.html", items=todos.find())

@app.get("/items/<ObjectId:id>")
def show_item(id):
    item = todos.find_one({"_id": id})
    return render_template("_item.html", item=item)

@app.post("/items")
def post_item():
    id = todos.insert_one({**request.form}).inserted_id
    return show_item(id)

@app.delete("/items/<ObjectId:id>")
def delete_item(id):
    todos.delete_one({"_id": id})
    return ""
