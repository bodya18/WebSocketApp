from services.UserService import UserService
from flask import Blueprint, request
import json


api_bp = Blueprint('api', __name__, template_folder='templates')

@api_bp.route('/users/add', methods=['POST'])
def add_user():
    user_name = request.args['name']
    user_email = request.args['email']
    user_id = UserService.addUser(user_name, user_email, role="User")
    id = dict(user_id=user_id)
    return id


@api_bp.route('/users/all', methods=['GET'])
def get_all():
    users = UserService.getAll()
    return json.dumps([user.serialize() for user in users])