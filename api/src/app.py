from flask import Flask
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

