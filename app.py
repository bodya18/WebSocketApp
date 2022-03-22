from flask import Flask, render_template
from flask_sock import Sock

from middleware.config import mysql_conf

app = Flask(__name__)
sock = Sock(app)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf

from controllers.register import register_page

app.register_blueprint(register_page, url_prefix='/')

USERS = set()

def addUser(websocket):
    USERS.add(websocket)

def removeUser(websocket):
    USERS.remove(websocket)
    websocket.close()

@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/test')
def echo(socket):
    try:
        addUser(socket)
        while True:
            data = socket.receive()
            [user.send(data) for user in USERS]
    finally:
        removeUser(socket)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="23765")