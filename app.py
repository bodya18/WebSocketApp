import json
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


from services.UserService import UserService

@socket.on('user_message')
def user_message(msg_text):
    messages = UserService.get_messages_by_userId(user_id=msg_text["user_id"])
    UserService.new_message(message=msg_text["message"], user_id=msg_text["user_id"])
    UserService.update_status('Actived', msg_text["user_id"])
    
    new_chat = False
    if messages == []:
        new_chat = True
    msg_text["new_chat"] = new_chat
    
    socket.emit('admin_response', msg_text)


@socket.on('admin_send_message')
def admin_send_message(msg_text):
    user = UserService.get_by_id(msg_text["user_id"])
    if user["socket"] is not None:
        socket.emit('user_response', msg_text)
    else:
        print("User is offline")
    UserService.new_message(message=msg_text["message"], user_id=msg_text["user_id"], status = "Admin")

@socket.on('connected')
def connected(user):
    currentSocketId = request.sid
    UserService.update_socket(socket=currentSocketId, id=user["id"])

@socket.on('disconnect')
def disconnect():
    currentSocketId = request.sid
    UserService.delete_socket(socket=currentSocketId)


if __name__ == '__main__':
    socket.run(app, host="0.0.0.0", port="23765", debug=True)
    # socket.run(app, debug=True)