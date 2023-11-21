from flask import Flask, request
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

@app.route("/items/create", methods=[ "POST" ])
def route_createItem():
    item = {
        'id' : request.json['id'],
        'type' : request.json['type'],
        'descricao' : request.json['descricao'],
        'categoria' : request.json['categoria'],
        'dataDeAquisicao' : request.json['dataDeAquisicao'],
        'estadoDeConservacao' : request.json['estadoDeConservacao'],
        'localizacao' : request.json['localizacao'],
        'uriImagem' : request.json['uriImagem']
    }
    return items.createItem(item)

@app.route("/items/update/<itemType>/<id>", methods=[ "PATCH" ])
def route_updateItem(itemType, id):
    item = items.getItem(id, itemType)
    for key,value in request.get_json().items():
        item[key] = value

    return items.updateItem(item)

@app.route("/items/delete/<itemType>/<id>", methods=[ "DELETE" ])
def route_deleteItem(itemType, id):
    item = items.getItem(id, itemType)
    items.deleteItem(id, itemType)
    return item