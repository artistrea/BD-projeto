import psycopg2
import psycopg2.extras

db = psycopg2.connect("postgresql://bd_projeto:123456@localhost:5436/bd_projeto_db")


def executeQuery(query: str, params=()) -> list:
    '''Create cursor and run query.

    Keyword arguments:
    query -- codigo SQL. Se tiver parametro, use "parametro"=%s 
    params -- se precisar passar parametros, os passe aqui em ordem. Serão usados para substituir os %s

    '''
    cur = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute(query, params)
    results = cur.fetchall()

    db.commit()

    cur.close()

    return results

def executeCommand(command: str, params=()) -> bool:
    cur = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(command, params)
    db.commit()
    cur.close()


