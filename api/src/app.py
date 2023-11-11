from flask import Flask
import routes.items as items
import sys

# setting path
sys.path.append('db')

app = Flask(__name__)

@app.route("/items", methods=[ "GET" ])
def getAllItemsRoute():
    return items.getAllItems()

@app.route("/items/<itemType>/<id>", methods=[ "GET" ])
def me_api(itemType, id):
    return items.getItem(id, itemType)
