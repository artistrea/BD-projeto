import db
import routes.auth as auth

def getAllLoans():
    loans = db.executeQuery('SELECT * FROM "Emprestimos" INNER JOIN "Usuarios" ON "Emprestimos"."userId" = "Usuarios"."id" ORDER BY "dataDeEmprestimo" DESC')
    return loans



def getLoanByUserId(user_id):
    loans = db.executeQuery('SELECT * FROM "Emprestimos" WHERE "userId"=%s ORDER BY "dataDeEmprestimo" DESC ', (user_id,))

    if len(loans) == 0:
        return None
    
    return loans

def getLoanByItemAndStatus(item_id, item_type, status):
    loans = db.executeQuery('SELECT * FROM "Emprestimos" WHERE "itemId"=%s AND "itemType"=%s AND "status"=%s ORDER BY "dataDeEmprestimo" DESC', (item_id,item_type, status))

    if len(loans) == 0:
        return None
    
    return loans

def getLoan(userId, itemId, itemType, dataDeEmprestimo):
    loan = db.executeQuery('SELECT * FROM "Emprestimos" WHERE "userId"=%s AND "dataDeEmprestimo"=%s AND "itemId"=%s AND "itemType"=%s', (userId, dataDeEmprestimo, itemId, itemType))

    if not loan:
        return None
    
    return loan[0]

create_loan_schema = {
    "type": "object",
    "properties": {
        "dataDeEmprestimo":         { "type": "string", "format": "date-time" },
        "dataDeDevolucaoPrevista":  { "type": "string", "format": "date-time" },
        "status":                   { "enum": ["emAndamento", "concluido", "pedido"] },
        "userId":                   { "type": "number" },
        "itemId":                   { "type": "number" },
        "itemType":                 { "enum": ["livro", "materialDidatico"] }
    },
    "required": ["dataDeEmprestimo","dataDeDevolucaoPrevista", "status"]
}

def createLoan(create_loan_info):
    fields = [key for key in create_loan_info.keys()]
    properties = ",".join(list(map(lambda x:  f'"{x}"', fields)))
    values = ",".join(list(map(lambda x: f"%({x})s", fields)))

    query = f"INSERT INTO \"Emprestimos\"({properties}) VALUES ({values}) RETURNING \"Emprestimos\".*;"

    new_loan =  auth.secure_format_loan(db.executeQuery(query, create_loan_info)[0])

    return new_loan



update_loan_schema = {
    "type": "object",
    "properties": {
        "dataDeEmprestimo":         { "type": "string", "format": "date-time" },
        "userId":                   { "type": 'number' },
        "dataDeDevolucaoPrevista":  { "type": "string", "format": "date-time" },
        "status":                   { "enum": ["emAndamento", "concluido", "pedido"] },
        "itemId":                   { "type": "number" },
        "itemType":                 { "enum": ["livro", "materialDidatico"] }
    },
}

def updateLoan(update_loan_info):
    updated_loan =  auth.secure_format_loan(db.executeQuery('''
        UPDATE "Emprestimos"
        SET 
            "dataDeDevolucaoPrevista"=%(dataDeDevolucaoPrevista)s,
            "status"=%(status)s
        WHERE "dataDeEmprestimo"=%(dataDeEmprestimo)s AND "userId"=%(userId)s AND "itemId"= %(itemId)s AND "itemType"=%(itemType)s
        RETURNING *;
        ''', update_loan_info
        )[0])

    return updated_loan



delete_loan_schema = {
    "type": "object",
    "properties": {
        "dataDeEmprestimo": { "type": "string", "format": "date-time" },
        "itemType":         { "enum": ["livro", "materialDidatico"] }
    },
    "required": ["dataDeEmprestimo", "itemType"]
}

def deleteLoan(user_id, data_de_emprestimo, item_id, item_type):
    response = db.executeQuery('''
        DELETE FROM "Emprestimos" WHERE "Emprestimos"."userId" = %s
        AND "Emprestimos"."dataDeEmprestimo" = %s
        AND "Emprestimos"."itemId" = %s
        AND "Emprestimos"."itemType" = %s
        RETURNING "Emprestimos".*''', (user_id, data_de_emprestimo, item_id, item_type)
    )

    return response

def acceptLoan(loan):
    db.executeCommand('''
                        UPDATE "Emprestimos"
                        SET 
                            "dataDeDevolucaoPrevista"=%(dataDeDevolucaoPrevista)s,
                            "status"=%(status)s
                        WHERE "dataDeEmprestimo"=%(dataDeEmprestimo)s AND "userId"=%(userId)s AND "itemId"=%{itemId}s AND "itemType=%{itemType}s    
                      ''', loan)
