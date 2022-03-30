from services.ChatService import ChatService
from services.UserService import UserService
from middleware.config import ROOT_DIR
from flask import Blueprint, render_template, request, session, redirect
import json


users_page = Blueprint('users', __name__, template_folder='templates')

@users_page.route('/add', methods=['POST'])
def add_user():
    user_name = request.json['name']
    print(user_name)
    user_id = UserService.addUser(user_name)
    id = dict(user_id=user_id)
    return id


@users_page.route('/api/all', methods=['GET'])
def get_all():
    _users = list()
    users = UserService.getAll()
    for user in users:
        _user = dict()
        user = user.__dict__
        _user["id"] = user['id']
        _user["status"] = user['status']
        _user["name"] = user['name']
        # _user["socket"] = user['socket']
        print(_user)
        
        _users.append(_user)
    return json.dumps(_users)