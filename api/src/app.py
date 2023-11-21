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
    item = request.json['item']
    item = {
        'id' : item['id'],
        'type' : item['type'],
        'descricao' : item['descricao'],
        'categoria' : item['categoria'],
        'dataDeAquisicao' : item['dataDeAquisicao'],
        'estadoDeConservacao' : item['estadoDeConservacao'],
        'localizacao' : item['localizacao'],
        'uriImagem' : item['uriImagem']
    }
    if item['type'] == 'livro':
        book = request.json['livro']
        book = {
            "ISBN" : book['ISBN'],
            "title" : book['title'],
            "author" : book['author'],
        }
        return items.createItem(item, book)
    elif item['type'] == 'materialDidatico':
        material = request.json['materialDidatico']
        material = {
            "id" : material['id'],
            "numeroDeSerie" : material['numeroDeSerie']
        }
        return items.createItem(item, material)

@app.route("/items/update/<itemType>/<id>", methods=[ "PATCH" ])
def route_updateItem(itemType, id):
    item = items.getItem(id, itemType)
    for key,value in request.json['item'].items():
        item[key] = value
    bookOrMaterial = item
    for key,value in request.json[itemType].items():
        bookOrMaterial[key] = value
    return items.updateItem(item, bookOrMaterial)

@app.route("/items/delete/<itemType>/<id>", methods=[ "DELETE" ])
def route_deleteItem(itemType, id):
    item = items.getItem(id, itemType)
    items.deleteItem(id, itemType)
    return item