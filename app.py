from flask import Flask, request, render_template
from flask_socketio import SocketIO

from middleware.config import mysql_conf

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf
app.secret_key = 'sdafjhdsakfdsndnnvcxbi2'

from controllers.users import api_bp
from controllers.admin import admin_bp

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")

USERS = []

@socket.on('message')
def message(msg_text):
    for user in USERS:
        if request.sid is not user:
            socket.emit('message_response', msg_text, room=user)

@socket.on('connect')
def connect():
    currentSocketId = request.sid
    USERS.append(currentSocketId)

@socket.on('disconnect')
def disconnect():
    currentSocketId = request.sid
    USERS.remove(currentSocketId)


if __name__ == '__main__':
    socket.run(app, host="0.0.0.0", port="23765", debug=True)
    # socket.run(app, debug=True)