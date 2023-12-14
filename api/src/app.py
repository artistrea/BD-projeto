from flask import Flask, request
import routes.items as items
import routes.auth as auth
import routes.users as users
import routes.loans as loans
import sys
from flask import request
import jsonschema
from datetime import datetime
from flask_cors import CORS, cross_origin

# setting path
sys.path.append('db')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def validate_json(json_to_validate, schema):
    try:
        jsonschema.validate(instance=json_to_validate, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


@app.route("/items", methods=[ "GET" ])
@cross_origin()
def getAllItemsRoute():
    return items.getAllItems()

@app.route("/items/<itemType>/<id>", methods=[ "GET" ])
@cross_origin()
def me_api(itemType, id):
    item = items.getItem(id, itemType)
    if item is None:
        return { "message" : "Item not found" }, 404
    return item

@app.route("/items/create", methods=[ "POST" ])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
def route_deleteItem(itemType, id):
    if not auth.authorize_chief():
        return { "message" : "Unauthorized" }, 401
    item = items.getItem(id, itemType)
    if item is None:
        return { "message": "Item not found" }, 404
    items.deleteItem(id, itemType)
    return item


@app.route("/items/search/<query>", methods=[ "GET" ])
@cross_origin()
def route_searchItems(query):
    return items.searchItem(query)

@app.route("/items/isAvailable/<itemType>/<id>", methods=[ "GET" ])
@cross_origin()
def route_item_isAvailabe(itemType, id):
    if loans.getLoanByItemAndStatus(id, itemType, "emAndamento"):
        return {'available' : False}
    return {'available' : True}

@app.route("/auth/login", methods=["POST"])
@cross_origin()
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
@cross_origin()
def logout_all_devices():
    logged_out = auth.logout()
    if not logged_out:
        return { "message": "Nao foi possivel fazer logout..." }, 401
    return { "message": "Deslogado em todos os aparelhos com sucesso!" }

@app.route("/user/atual", methods=[ "POST" ])
@cross_origin()
def get_current_user():
    user = auth.get_current_user()

    if user is None: 
        return { "message": "Unauthorized" }, 401

    return user

@app.route("/users", methods=[ "GET" ])
@cross_origin()
def getAllUsersRoute():
    is_at_least_chief = auth.authorize_chief()

    if not is_at_least_chief:
        return { "message": "Unauthorized" }, 401

    data = users.getAllUsers()
    return data


@app.route("/user/<id>", methods=[ "GET" ])
@cross_origin()
def getUserRoute(id):
    cur_user = auth.get_current_user()

    if cur_user is None:
        return { "message": "Unauthorized" }, 401
    
    if auth.authorize_chief(cur_user):
        usr = users.getUser(id)
        if usr is None:
            return { "message": "Not found" }, 404
        
        return usr

    if cur_user["id"] == id:
        return cur_user

    return { "message": "Unauthorized" }, 401

@app.route("/user", methods=[ "POST" ])
@cross_origin()
def createUserRoute():
    body = request.json

    if not auth.authorize_admin():
        return { "message": "Unauthorized" }, 401

    if not validate_json(body, users.create_user_schema):
        return { "message": "Invalid parameters" }, 400

    newUser = users.createUser(body)

    return newUser

@app.route("/user/<id>", methods=[ "DELETE" ])
@cross_origin()
def deleteUserRoute(id):
    cur_user = auth.get_current_user()

    can_delete = cur_user is not None and (auth.authorize_admin(cur_user) or id == cur_user["id"])

    if not can_delete:
        return { "message": "Unauthorized" }, 401

    deletedUser = users.deleteUser(id)

    if deletedUser is None: 
        return { "message": "Not Found" }, 404

    return deletedUser


@app.route("/user/<id>", methods=[ "PUT" ])
@cross_origin()
def updateUserRoute(id):
    cur_user = auth.get_current_user()

    if cur_user is None: return { "message": "Unauthorized" }, 401

    can_edit = auth.authorize_admin(cur_user) or str(cur_user["id"]) == id

    if not can_edit: return { "message": "Unauthorized" }, 401

    body = request.json

    if not validate_json(body, users.update_user_schema):
        return { "message": "Invalid parameters" }, 400
    
    user = users.getUser(id)

    if user is None: return { "message": "Not Found" }, 404

    newUser = users.updateUser({ **user, **body })

    return newUser

@app.route("/user/<id>/function", methods=[ "PUT" ])
@cross_origin()
def updateUserFunctionRoute(id):
    cur_user = auth.get_current_user()

    can_edit = auth.authorize_admin(cur_user)

    if not can_edit: return { "message": "Unauthorized" }, 401

    body = request.json

    if not validate_json(body, users.update_user_function_schema):
        return { "message": "Invalid parameters" }, 400

    user = users.getUser(id)

    if user is None: return { "message": "Not Found" }, 404


    newUser = users.updateUserFunction({ **user, **body })

    return newUser


@app.route("/user/<id>/password", methods=[ "PUT" ])
@cross_origin()
def updateUserPasswordRoute(id):
    body = request.json

    cur_user = auth.get_current_user()

    if auth.authorize_admin(cur_user):
        if not validate_json(body, users.update_user_password_schema):
            return { "message": "Invalid parameters" }, 400

        user = users.getUser(id)

        if user is None: return { "message": "Not Found" }, 404

        return users.updateUserPassword(id, body["senha"]["nova"])

    session = auth.login(update_user_password_info["login"], update_user_password_info["senha"]["antiga"])

    can_edit = session is not None and session["user"]["id"] == cur_user["id"]

    if not can_edit: return { "message": "Unauthorized" }, 401

    newUser = users.updateUserPassword(id, body["senha"]["nova"])

    return newUser


@app.route("/loan", methods=[ "GET" ])
@cross_origin()
def getAllLoansRoute():

    return loans.getAllLoans()


@app.route("/loan/<id>", methods=[ "GET" ])
@cross_origin()
def getLoanRoute(id):
    cur_user = auth.get_current_user()

    if cur_user is None:
        return { "message": "Unauthorized" }, 401
    
    if auth.authorize_chief(cur_user) or str(cur_user['id']) == id:
        lns = loans.getLoanByUserId(id)
        if lns is None:
            return { "message": "Not found" }, 404

        return lns

    return { "message": "Unauthorized" }, 401


@app.route("/loan", methods=[ "POST" ])
@cross_origin()
def createLoanRoute():
    body = request.json

    # if not auth.authorize_admin():
    #     return { "message": "Unauthorized" }, 401

    if not validate_json(body, loans.create_loan_schema):
        return { "message": "Invalid parameters" }, 400

    new_loan = loans.createLoan(body)

    return new_loan


@app.route("/loan/<user_id>/<item_id>", methods=[ "DELETE" ])
@cross_origin()
def deleteLoanRoute(user_id, item_id):
    body = request.json

    if not validate_json(body, loans.delete_loan_schema):
        return { "message": "Invalid parameters" }, 400
    
    deleted_loan = loans.deleteLoan(user_id, body["dataDeEmprestimo"], item_id, body["itemType"])

    return deleted_loan


@app.route("/loan/<user_id>", methods=[ "PUT" ])
@cross_origin()
def updateLoanRoute(user_id):
    user_id = int(user_id)
    cur_user = auth.get_current_user()

    if cur_user is None: return { "message": "Unauthorized" }, 401

    can_edit = auth.authorize_chief(cur_user) or str(cur_user["id"]) == user_id

    if not can_edit: return { "message": "Unauthorized" }, 401

    body = request.json
    loan_group = loans.getLoanByUserId(user_id)

    if loan_group is None: return { "message": "Not Found" }, 404

    for loan in loan_group:
        data_obj = datetime.strptime(str(loan["dataDeEmprestimo"]), "%Y-%m-%d")
        formated_date = data_obj.strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        if body["dataDeEmprestimo"] == formated_date:

            loan_date = body["dataDeEmprestimo"]
            body.pop("dataDeEmprestimo")
            break


    if not validate_json(body, loans.update_loan_schema):
        return { "message": "Invalid parameters" }, 400
    
    body["userId"] = user_id
    body["dataDeEmprestimo"] = loan_date


    updated_loan = loans.updateLoan(body)

    return updated_loan

@app.route("/loan/<userId>/<itemId>/<itemType>", methods=[ "PUT" ])
@cross_origin()
def acceptLoanRoute(userId, itemId, itemType):
    if not auth.authorize_chief():
        return { "message" : "Unauthorized" }, 401
    body = request.json
    valid_body = validate_json(body, loans.update_loan_schema)

    dataDeEmprestimo = body['dataDeEmprestimo']
    if not valid_body:
        return { "message": "Wrong parameters" }, 400
    
    loan = loans.getLoan(userId, itemId, itemType, dataDeEmprestimo)

    for key,value in body.items():
        loan[key] = value

    return loans.updateLoan(loan)