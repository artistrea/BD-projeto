# importing
import db

def getAllItems():
    items = db.executeQuery('SELECT * FROM "Items"')

    return items

def getItem(id, itemType):
    items = db.executeQuery('SELECT * FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))

    return items[0]

def createItem(item: dict):
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

def updateItem(item: dict):

    succeded = db.executeCommand(f'''UPDATE "Items"
                                SET 
                                    "descricao"=%(descricao)s, 
                                    "categoria"=%(categoria)s, 
                                    "dataDeAquisicao"=%(dataDeAquisicao)s, 
                                    "estadoDeConservacao"=%(estadoDeConservacao)s, 
                                    "localizacao"=%(localizacao)s, 
                                    "uriImagem"=%(uriImagem)s
                                WHERE "id"=%(id)s AND "type"=%(type)s''', item)

    if not succeded:
        raise RuntimeError('Update Item operation failed.')
    return item

def deleteItem(id, itemType):
    succeded = db.executeCommand('DELETE FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))
    if not succeded:
        raise RuntimeError('Delete Item operation failed.')
    return {"id":id, "type":itemType}