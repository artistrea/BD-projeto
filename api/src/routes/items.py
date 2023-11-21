# importing
import db

def getAllItems():
    items = db.executeQuery('SELECT * FROM "Items"')

    return items

def getItem(id, itemType):
    if itemType == 'livro':
        items = db.executeQuery('SELECT * FROM "Items" INNER JOIN "Livros" ON "Items"."id"="Livros"."ISBN" WHERE "Items"."id"=%s AND "Items"."type"=%s', (id, itemType))
    elif itemType == 'materialDidatico':
        items = db.executeQuery('SELECT * FROM "Items" INNER JOIN "MateriaisDidaticos" ON "Items"."id"="MateriaisDidaticos"."id" WHERE "Items"."id"=%s AND "Items"."type"=%s', (id, itemType))
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
        return {'item':item, 'livro':bookOrmaterial}
    elif item['type'] == 'materialDidatico':
        db.executeCommand('''
                          INSERT INTO "MateriaisDidaticos" ("id", "numeroDeSerie")
                          VALUES
                          (%(id)s, %(numeroDeSerie)s)
                          ''', bookOrmaterial)
        return {'item':item, 'materialDidatico':bookOrmaterial}

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
        return {'item':item, 'livro':bookOrmaterial}
    elif item['type'] == 'materialDidatico':
        db.executeCommand('''UPDATE "MateriaisDidaticos"
                            SET
                                "numeroDeSerie"=%(numeroDeSerie)s
                            WHERE "id"=%(id)s AND "type"=%(type)s
                          ''', bookOrmaterial)
        return {'item':item, 'materialDidatico':bookOrmaterial}

def deleteItem(id, itemType):
    db.executeCommand('DELETE FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))
    return {"id":id, "type":itemType}