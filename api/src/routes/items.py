# importing
import db

def getAllItems():
    items = db.executeQuery('SELECT * FROM "Items"')

    return items

def getItem(id, itemType):
    items = db.executeQuery('SELECT * FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))

    return items[0]

def createItem(item: dict):
    db.executeCommand('''INSERT INTO "Items" 
                        ("id", "type", "descricao", "categoria", "dataDeAquisicao",
                        "estadoDeConservacao", "localizacao", "uriImagem") 
                        VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (
                            item['id'], item['type'], item['descricao'], item['categoria'], item['dataDeAquisicao'],
                            item['estadoDeConservacao'], item['localizacao'], item['uriImagem']
                        ))
    return item

def updateItem(item: dict):
    db.executeCommand(f'''UPDATE "Items"
                                SET 
                                    "descricao"=%(descricao)s, 
                                    "categoria"=%(categoria)s, 
                                    "dataDeAquisicao"=%(dataDeAquisicao)s, 
                                    "estadoDeConservacao"=%(estadoDeConservacao)s, 
                                    "localizacao"=%(localizacao)s, 
                                    "uriImagem"=%(uriImagem)s
                                WHERE "id"=%(id)s AND "type"=%(type)s''', item)

    return item

def deleteItem(id, itemType):
    db.executeCommand('DELETE FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))
    return {"id":id, "type":itemType}