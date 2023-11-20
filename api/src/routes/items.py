import db

def getAllItems():
    books = db.executeQuery('SELECT * FROM "Items" INNER JOIN "Livros" ON "Livros"."ISBN" = "Items"."id" AND "Livros"."type" = "Items"."type"')

    materials = db.executeQuery('SELECT * FROM "Items" INNER JOIN "MateriaisDidaticos" ON "MateriaisDidaticos"."id" = "Items"."id" AND "MateriaisDidaticos"."type" = "Items"."type"')

    return [*books, *materials]

def getItem(id, itemType):
    items = db.executeQuery('SELECT * FROM "Items" WHERE "id"=%s AND "type"=%s', (id, itemType))

    return items[0]
