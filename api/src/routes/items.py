# importing
import db

def getAllItems():
    items = db.executeQuery('SELECT * FROM "Items"')

    return items

def getItem(id, itemType):
    items = db.executeQuery('SELECT * FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))

    return items[0]

def createItem(item):
    succeded = db.executeCommand('''INSERT INTO "Items" 
                        ("id", "type", "descricao", "categoria", "dataDeAquisicao",
                        "estadoDeConservacao", "localizacao", "uriImagem") 
                        VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (
                            item['id'], item['type'], item['descricao'], item['categoria'], item['dataDeAquisicao'],
                            item['estadoDeConservacao'], item['localizacao'], item['uriImagem']
                        ))
    if not succeded:
        raise RuntimeError('Create Item operation failed.')
    return item