from flask import Flask, request
from flask_socketio import SocketIO

from middleware.config import mysql_conf

app = Flask(__name__)
socket = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf
app.secret_key = 'sdafjhdsakfdsndnnvcxbi2'

from controllers.chats import chats_page
from controllers.users import users_page

app.register_blueprint(chats_page, url_prefix='/')
app.register_blueprint(users_page, url_prefix='/user')


USERS = []

def addUser(websocket):
    USERS.append(websocket)

def removeUser(websocket):
    USERS.remove(websocket)


@socket.on('message')
def message(msg_text):
    for user in USERS:
        if request.sid is not user:
            socket.emit('message_response', msg_text, room=user)

@socket.on('connect')
def connect():
    currentSocketId = request.sid
    addUser(currentSocketId)

@socket.on('disconnect')
def disconnect():
    currentSocketId = request.sid
    removeUser(currentSocketId)


if __name__ == '__main__':
    socket.run(app, host="0.0.0.0", port="23765")
    # socket.run(app, debug=True)