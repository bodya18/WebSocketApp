from services.UserService import UserService
from flask import Blueprint, request
import json


api_bp = Blueprint('api', __name__, template_folder='templates')

@api_bp.route('/users/add', methods=['POST'])
def add_user():
    user_name = request.args['name']
    user_email = request.args['email']
    user = UserService.addUser(user_name, user_email, role="User")
    return user


@api_bp.route('/users/all', methods=['GET'])
def get_all():
    users = UserService.getAll()
    return json.dumps([user.serialize() for user in users])


@api_bp.route('/users/all/status', methods=['GET'])
def get_by_status():
    status = request.args['status']
    users = UserService.getStatus(status)
    return json.dumps([user.serialize() for user in users])


@api_bp.route('/users/new/status', methods=['POST'])
def update_status():
    status = request.args['status']
    id = request.args['id']
    user = UserService.update_status(status, id)
    return user