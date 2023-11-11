from flask import Flask
from routes.items.index import getAllItems

app = Flask(__name__)

@app.route("/", methods=[ "POST" ])
def me_api():
    return getAllItems()
