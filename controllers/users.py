from Auth import auth_required
from middleware.config import STATUS_LIST
from services.UserService import UserService
from flask import Blueprint, request
import json


api_bp = Blueprint('api', __name__, template_folder='templates')

@api_bp.route('/users/add', methods=['POST'])
def add_user():
    try:
        if len(request.args['name'])<2 or len(request.args['name'])>15:
            return {"error": "length name need min 2 and max 15"}
        user_name = request.args['name']
        user_email = request.args['email']
        user = UserService.get_by_email(user_email)
        if user is None:
            user = UserService.addUser(user_name, user_email, role="User")
            return user
        elif user.name == user_name:
            return user.serialize()
        else: 
            return dict(error="invalid name")
    except Exception as e:
        print(e)
        return dict(error="need in params name and email")

# пагинацию
@api_bp.route('/users/all', methods=['GET'])
@auth_required("BEARER")
def get_all():
    users = UserService.getAll()
    page = int(request.args['page']) if 'page' in request.args else 1
    limit = int(request.args['limit']) if 'limit' in request.args else 100

    users = users[page*limit-limit:page*limit]
    return json.dumps([user.serialize() for user in users])


@api_bp.route('/users/all/status', methods=['GET'])
@auth_required("BEARER")
def get_by_status():
    try:
        status = request.args['status']
        if status in STATUS_LIST:
            users = UserService.getStatus(status)
            page = int(request.args['page']) if 'page' in request.args else 1
            limit = int(request.args['limit']) if 'limit' in request.args else 100
            users = users[page*limit-limit:page*limit]

            return json.dumps([user.serialize() for user in users])
        else:
            return dict(error="Status not valid")
    except:
        return dict(error="need in params status")


@api_bp.route('/users/messages', methods=['GET'])
@auth_required("BEARER")
def get_all_msg():
    try:
        user_id = request.args['user_id']
        messages = UserService.get_messages_by_userId(user_id)
        return json.dumps([msg.serialize() for msg in messages])
    except:
        return dict(error="need in params user_id")


@api_bp.route('/users/new/status', methods=['POST'])
@auth_required("BEARER")
def update_status():
    try:
        status = request.args['status']
        id = request.args['id']
        user = UserService.update_status(status, id)
        return user
    except:
        return dict(error="need in params status, id")