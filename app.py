from flask import Flask, request
from flask_restx import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from services.UserService import UserService
from middleware.config import mysql_conf, log

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf
app.config['RESTPLUS_VALIDATE'] = True

app.secret_key = 'sdafjhdsakfdsndnnvcxbi2'

api = Api(app, version='mine', title='Just API', doc="/swagger")

from controllers.users import ns as UserApiNs
from controllers.admin import ns as AdminApiNs

api.add_namespace(UserApiNs)
api.add_namespace(AdminApiNs)

@socket.on('user_message')
def user_message(msg_text):
    try:
        log.info(msg_text)
        current_user = UserService.get_by_id(msg_text["user_id"])
        if current_user is not None and current_user.status == "Banned":
            return socket.emit('user_response', dict(error="User banned"))
        user = UserService.update_status('Actived', msg_text["user_id"])
        if user:
            messages = UserService.get_messages_by_userId(user_id=msg_text["user_id"])
            UserService.new_message(message=msg_text["message"], user_id=msg_text["user_id"], file = msg_text["file"] or None)

            msg_text["new_chat"] = True if messages == [] else False
            socket.emit('admin_response', msg_text)
        else:
            socket.emit('user_response', dict(error="User is not defined"))
    except Exception as e:
        log.error(e)
        socket.emit('user_response', dict(error="invalid json format, need user_id and message"))


@socket.on('admin_send_message')
def admin_send_message(msg_text):
    try:
        log.info(msg_text)
        user = UserService.get_by_id(msg_text["user_id"])
        if user:
            if user["socket"] is not None:
                socket.emit('user_response', msg_text, room=user["socket"])
            else:
                log.info('=======User is offline=======')
            UserService.new_message(message=msg_text["message"], user_id=msg_text["user_id"], file = msg_text["file"] or None, status = "Admin")
        else:
            socket.emit('admin_response', dict(error="User is not defined"))
    except Exception as e:
        log.error(e)
        socket.emit('admin_response', dict(error="invalid json format, need user_id and message"))


@socket.on('connected')
def connected(user):
    log.info(user)
    currentSocketId = request.sid
    log.info(f"connect: {currentSocketId}")
    try:
        UserService.update_socket(socket=currentSocketId, id=user["id"])
    except Exception as e:
        log.error(e)

@socket.on('disconnect')
def disconnect():
    log.info(f"disconnect: {request.sid}")
    currentSocketId = request.sid
    UserService.delete_socket(socket=currentSocketId)


if __name__ == '__main__':
    socket.run(app, host="0.0.0.0", port="23765", debug=True, log_output=False)