# importing
import db

def getAllItems():
    items = db.executeQuery('SELECT * FROM "Items"')

    return items

def getItem(id, itemType):
    items = db.executeQuery('SELECT * FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))

    return items[0]
