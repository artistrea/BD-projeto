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
    item = items.getItem(id, itemType)
    if item is None:
        return { "message" : "Item not found" }, 404
    return item

@app.route("/items/create", methods=[ "POST" ])
def route_createItem():
    if not auth.authorize_chief():
        return { "message" : "Unauthorized" }, 401
    body = request.json
    valid_body = validate_json(body, items.create_item_schema)
    if not valid_body:
        return { "message": "Wrong parameters" }, 400
    item = body['item']
    item_type = item['type']
    bookOrMaterial = body[item_type]

    bookOrMaterial_idName = "ISBN" if item_type == 'livro' else 'id'
    if item["id"] != bookOrMaterial[bookOrMaterial_idName]:
        return { "message": "Wrong parameters" }, 400
    
    try:
        newItem = items.createItem(item, bookOrMaterial)
        return newItem
    except:
        return { "message": "Could not create the item" }, 400

@app.route("/items/update/<itemType>/<id>", methods=[ "PATCH" ])
def route_updateItem(itemType, id):
    if not auth.authorize_chief():
        return { "message" : "Unauthorized" }, 401
    body = request.json
    valid_body = validate_json(body, items.update_item_schema)
    if not valid_body:
        return { "message": "Wrong parameters" }, 400

    item = items.getItem(id, itemType)
    if item is None:
        return { "message": "Item not found" }, 404

    for key,value in body.items():
        item[key] = value
    bookOrMaterial = item
    return items.updateItem(item, bookOrMaterial)

@app.route("/items/delete/<itemType>/<id>", methods=[ "DELETE" ])
def route_deleteItem(itemType, id):
    if not auth.authorize_chief():
        return { "message" : "Unauthorized" }, 401
    item = items.getItem(id, itemType)
    if item is None:
        return { "message": "Item not found" }, 404
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
