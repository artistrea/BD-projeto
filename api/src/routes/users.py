import db
import routes.auth as auth

def getAllUsers():
    users = db.executeQuery('''
    SELECT * FROM "Usuarios"
    ''')
    return [auth.secure_format_user(user) for user in users]

def getUser(id):
    users = db.executeQuery('''
    SELECT * FROM "Usuarios" WHERE "id"=%s
    ''', (id,))

    if len(users) == 0:
        return None
    
    return users[0]

def deleteUser(id):
    response = db.executeQuery('''
        DELETE FROM "Usuarios"
        WHERE "id"=%s
        RETURNING "Usuarios".*
        ''', id
    )
    if len(response) > 0:
        return auth.secure_format_user(response[0])

    return None


create_user_schema = {
    "type": "object",
    "properties": {
        "login": { "type": "string" },
        "uriImagem": { "type": "string"  },
        "nome": { "type": "string" },
        "sobrenome": { "type": "string" },
        "funcao": {
            "enum": ["administrador", "chefe", "estudante"],
        },
        "senha": { "type": "string" },
    },
    "required": ["login", "senha", "nome", "sobrenome"],
    "additionalProperties": False
}



def createUser(create_user_info):
    fields = [key for key in create_user_info.keys()]
    properties = ",".join(list(map(lambda x: '"hashSenha"' if x == "senha" else '"' + x + '"', fields)))
    values = ",".join(list(
        map(lambda x: "crypt(%(" + x + ")s, gen_salt('bf'))" if x == "senha" else "%(" + x + ")s", fields)
        ))

    query = f"INSERT INTO \"Usuarios\"({properties}) VALUES ({values}) RETURNING \"Usuarios\".*;"

    newUser =  auth.secure_format_user(db.executeQuery(query, create_user_info)[0])

    return newUser


update_user_schema = {
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "uriImagem": { "type": "string"  },
        "nome": { "type": "string" },
        "sobrenome": { "type": "string" },
    },
    "additionalProperties": False
}


def updateUser(update_user_info):
    newUser =  auth.secure_format_user(db.executeQuery('''
        UPDATE "Usuarios"
        SET 
            "uriImagem"=%(uriImagem)s, 
            "nome"=%(nome)s, 
            "sobrenome"=%(sobrenome)s
        WHERE "id"=%(id)s
        RETURNING "Usuarios".*;
        ''', update_user_info
        )[0])

    return newUser


update_user_function_schema = {
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "funcao": {
            "enum": ["administrador", "chefe", "estudante"],
        },
    },
    "required": ["id", "funcao"],
    "additionalProperties": False
}

def updateUserFunction(update_user_function_info):
    newUser =  auth.secure_format_user(db.executeQuery('''
        UPDATE "Usuarios"
        SET 
            "funcao"=%(funcao)s
        WHERE "id"=%(id)s
        RETURNING "Usuarios".*;
        ''', update_user_function_info
        )[0])

    return newUser
    

update_user_password_schema = {
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "senha": {
            "type": "object",
            "properties": {
                "antiga": { "type": "string" },
                "nova": { "type": "string" },
            },
            "required": ["nova"]
        },
    },
    "required": ["id", "senha"],
    "additionalProperties": False
}

def updateUserPassword(id, newPassword):
    newUser =  auth.secure_format_user(db.executeQuery('''
        UPDATE "Usuarios"
        SET "senha"=crypt(%s, gen_salt('bf'))
        WHERE "id"=%s
        RETURNING "Usuarios".*;
        ''', (newPassword, id)
        )[0])

    return newUser


