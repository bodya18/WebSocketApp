from flask import Flask, render_template
from flask_sock import Sock

from middleware.config import mysql_conf

app = Flask(__name__)
sock = Sock(app)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf
app.secret_key = 'sdafjhdsakfdsndnnvcxbi2'

from controllers.chats import chats_page
from controllers.users import users_page

app.register_blueprint(chats_page, url_prefix='/')
app.register_blueprint(users_page, url_prefix='/user')

USERS = set()

def addUser(websocket):
    USERS.add(websocket)

def removeUser(websocket):
    USERS.remove(websocket)
    websocket.close()

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
    # app.run(host="0.0.0.0", port="23765")
    app.run(debug=True)