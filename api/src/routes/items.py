import db

update_item_schema = {
    "type": "object",
    "properties": {
        'id' :                  {"not" : {}}, #  Proibindo ele de tentar atualizar o id
        'type' :                {"not" : {}}, #  Proibindo ele de tentar atualizar o type
        'ISBN' :                {"not" : {}}, #  Proibindo ele de tentar atualizar o ISBN, se for um livro
        'descricao' :           { "type": "string" },
        'categoria' :           { "type": "string" },
        'dataDeAquisicao' :     { "type": "string" },
        'estadoDeConservacao' : { "type": "string" },
        'localizacao' :         { "type": "string" },
        'uriImagem' :           { "type": "string" },
        "title" :               { "type": "string" },
        "author" :              { "type": "string" },
        "numeroDeSerie":        { "type": "number" },
    },
}

create_item_schema = {
    "type": "object",
    "properties": {
        'item': {
            "type": "object",
            "properties": {
                'id' :                  { "type": "number" },
                'type' :                { "enum": ["livro", "materialDidatico"] },
                'descricao' :           { "type": "string" },
                'categoria' :           { "type": "string" },
                'dataDeAquisicao' :     { "type": "string" },
                'estadoDeConservacao' : { "type": "string" },
                'localizacao' :         { "type": "string" },
                'uriImagem' :           { "type": "string" }
            },
            "required": ["id", "type", "descricao", "categoria", "dataDeAquisicao", "estadoDeConservacao", "localizacao", "uriImagem"]
        },
        'livro': {
            "type": "object",
            "properties": {
                "ISBN" :                { "type": "number" },
                "title" :               { "type": "string" },
                "author" :              { "type": "string" },
            },
            "required": ["ISBN", "title", "author"]
        },
        'materialDidatico': {
            "type": "object",
            "properties": {
                "id" :                  { "type": "number" },
                "numeroDeSerie":        { "type": "number" },
            },
            "required": ["id", "numeroDeSerie"]
        }
    },
    "anyOf": [
        {
            "properties": {
                "item": {
                    "properties": {
                        "type": {"const": "livro"}
                    }
                }
            },
            "required": ["livro"]
        },
        {
            "properties": {
                "item": {
                    "properties": {
                        "type": {"const": "materialDidatico"}
                    }
                }
            },
            "required": ["materialDidatico"]
        }
    ],
    "required": ["item"],
}

def getAllItems():
    books = db.executeQuery('SELECT * FROM "Items" INNER JOIN "Livros" ON "Livros"."ISBN" = "Items"."id" AND "Livros"."type" = "Items"."type"')

    materials = db.executeQuery('SELECT * FROM "Items" INNER JOIN "MateriaisDidaticos" ON "MateriaisDidaticos"."id" = "Items"."id" AND "MateriaisDidaticos"."type" = "Items"."type"')

    return [*books, *materials]

def getItem(id, itemType):
    if itemType == 'livro':
        items = db.executeQuery('SELECT * FROM "Items" INNER JOIN "Livros" ON "Items"."id"="Livros"."ISBN" WHERE "Items"."id"=%s AND "Items"."type"=%s', (id, itemType))
    elif itemType == 'materialDidatico':
        items = db.executeQuery('SELECT * FROM "Items" INNER JOIN "MateriaisDidaticos" ON "Items"."id"="MateriaisDidaticos"."id" WHERE "Items"."id"=%s AND "Items"."type"=%s', (id, itemType))
    
    if not items:
        return None

    return items[0]

def createItem(item: dict, bookOrmaterial: dict):
    db.executeCommand('''INSERT INTO "Items" 
                        ("id", "type", "descricao", "categoria", "dataDeAquisicao",
                        "estadoDeConservacao", "localizacao", "uriImagem") 
                        VALUES 
                        (%(id)s, %(type)s, %(descricao)s, %(categoria)s, %(dataDeAquisicao)s,
                             %(estadoDeConservacao)s, %(localizacao)s, %(uriImagem)s)''', 
                        item)
    if item['type'] == 'livro':
        db.executeCommand('''
                          INSERT INTO "Livros" ("ISBN", "title", "author")
                          VALUES
                          (%(ISBN)s, %(title)s, %(author)s)
                          ''', bookOrmaterial)
    elif item['type'] == 'materialDidatico':
        db.executeCommand('''
                          INSERT INTO "MateriaisDidaticos" ("id", "numeroDeSerie")
                          VALUES
                          (%(id)s, %(numeroDeSerie)s)
                          ''', bookOrmaterial)
    return getItem(item['id'], item['type'])

def updateItem(item: dict, bookOrmaterial: dict):
    db.executeCommand('''UPDATE "Items"
                                SET 
                                    "descricao"=%(descricao)s, 
                                    "categoria"=%(categoria)s, 
                                    "dataDeAquisicao"=%(dataDeAquisicao)s, 
                                    "estadoDeConservacao"=%(estadoDeConservacao)s, 
                                    "localizacao"=%(localizacao)s, 
                                    "uriImagem"=%(uriImagem)s
                                WHERE "id"=%(id)s AND "type"=%(type)s''', item)
    if item['type'] == 'livro':
        db.executeCommand('''UPDATE "Livros"
                                SET
                                    "title"=%(title)s,
                                    "author"=%(author)s
                                WHERE "ISBN"=%(ISBN)s AND "type"=%(type)s
                          ''', bookOrmaterial)
    elif item['type'] == 'materialDidatico':
        db.executeCommand('''UPDATE "MateriaisDidaticos"
                            SET
                                "numeroDeSerie"=%(numeroDeSerie)s
                            WHERE "id"=%(id)s AND "type"=%(type)s
                          ''', bookOrmaterial)
    return getItem(item['id'], item['type'])

def deleteItem(id, itemType):
    db.executeCommand('DELETE FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))
    return {"id":id, "type":itemType}