import db
from flask import request

login_schema = {
    "type": "object",
    "properties": {
        "login": { "type": "string" },
        "password": { "type": "string"  },
    },
    "required": ["login", "password"],
}

def secure_format_user(unformatted_user):
    return {
        "id": unformatted_user["id"],
        "login": unformatted_user["login"],
        "nome": unformatted_user["nome"],
        "sobrenome": unformatted_user["sobrenome"],
        "funcao": unformatted_user["funcao"],
        "uriImagem": unformatted_user["uriImagem"],
    }

def secure_format_loan(unformatted_loan):
    return {
        "dataDeDevolucaoPrevista": unformatted_loan["dataDeDevolucaoPrevista"],
        "dataDeEmprestimo": unformatted_loan["dataDeEmprestimo"],
        "itemId": unformatted_loan["itemId"],
        "itemType": unformatted_loan["itemType"],
        "status": unformatted_loan["status"],
        "userId": unformatted_loan["userId"],
    }

def login(login, password):
    response_arr = db.executeQuery('SELECT * FROM "Usuarios" WHERE "Usuarios"."login" = %s AND "Usuarios"."hashSenha" = crypt(%s, "Usuarios"."hashSenha");', (login, password))

    if not len(response_arr):
        return None

    authentication_token = response_arr[0]["authToken"]

    return {
        "authentication_token": authentication_token,
        "user": secure_format_user(response_arr[0])
    }

def logout():
    user = dangerously_get_current_user()
    if user is None:
        return False

    db.executeCommand('UPDATE "Usuarios" SET "authToken" = uuid_generate_v4() WHERE "Usuarios"."authToken" = %s AND "Usuarios"."login" = %s;', (user["authToken"], user["login"]))

    return True


PERMISSIONS_HIERARCHY = {
    'estudante': 0,
    'chefe': 1,
    'administrador': 2,
}

def get_current_user():
    user = dangerously_get_current_user()

    if user is None: return None

    return secure_format_user(user)

def dangerously_get_current_user():
    authentication_token = request.headers.get("X-Auth-Token")
    if authentication_token is None or len(authentication_token) != 36:
        return None
    login = request.headers.get("X-Auth-Login")
    response_arr = db.executeQuery('SELECT * FROM "Usuarios" WHERE "Usuarios"."authToken" = %s AND "Usuarios"."login" = %s;', (authentication_token, login))

    if not len(response_arr):
        return None

    return response_arr[0]

def authorize_user(user=None):
    if user is None: user = get_current_user()

    return not (user is None)

def authorize_chief(user=None):
    if user is None: user = get_current_user()

    if user is None:
        return False

    return PERMISSIONS_HIERARCHY[user["funcao"]] >= PERMISSIONS_HIERARCHY["chefe"]

def authorize_admin(user=None):
    if user is None: user = get_current_user()

    if user is None:
        return False

    return PERMISSIONS_HIERARCHY[user["funcao"]] >= PERMISSIONS_HIERARCHY["administrador"]

