from flask import Flask, request, render_template, make_response
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
    if int(request.form["priority"]) > 5:
        # one way to handle errors: special headers for htmx
        headers = {'HX-Retarget': '#err', 'HX-Reswap': 'innerhtml'}
        return "Bad priority", 200, headers
    if request.form["priority"] == "0":
        # other: return err status code, have event handler in html
        return "Priority zero meltdown", 400
    id = todos.insert_one({**request.form}).inserted_id
    item = todos.find_one({"_id": id})
    return render_template("_item.html", item=item), 201

@app.delete("/items/<ObjectId:id>")
def delete_item(id):
    todos.delete_one({"_id": id})
    return ""
