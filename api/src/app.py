from flask import Flask, request
import routes.items as items
import routes.auth as auth
import sys
from flask import request
import jsonschema

# setting path
sys.path.append('db')

app = Flask(__name__)

def validate_json(json_to_validate, schema):
    try:
        jsonschema.validate(instance=json_to_validate, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


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
    body = request.json
    valid_body = validate_json(body, items.update_item_schema)
    if not valid_body:
        return { "message": "Wrong parameters" }, 400

    item = items.getItem(id, itemType)
    if not item:
        return { "message": "Item not found" }, 404

    for key,value in body.items():
        item[key] = value
    bookOrMaterial = item
    items.updateItem(item, bookOrMaterial)
    return items.getItem(id, itemType)

@app.route("/items/delete/<itemType>/<id>", methods=[ "DELETE" ])
def route_deleteItem(itemType, id):
    item = items.getItem(id, itemType)
    items.deleteItem(id, itemType)
    return item

@app.route("/auth/login", methods=["POST"])
def login():
    body = request.json
    valid_body = validate_json(body, auth.login_schema)

    if not valid_body:
        return { "message": "Wrong parameters" }, 400

    session = auth.login(body["login"], body["password"])

    if session is None:
        return { "message": "Unauthorized" }, 401

    return session

@app.route("/auth/logout_em_todos_aparelhos", methods=[ "POST" ])
def logout_all_devices():
    logged_out = auth.logout()
    if not logged_out:
        return { "message": "Nao foi possivel fazer logout..." }, 401
    return { "message": "Deslogado em todos os aparelhos com sucesso!" }

@app.route("/user/atual", methods=[ "POST" ])
def get_current_user():
    user = auth.get_current_user()

    if user is None: 
        return { "message": "Unauthorized" }, 401

    return user
