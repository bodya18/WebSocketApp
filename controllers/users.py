from services.ChatService import ChatService
from services.UserService import UserService
from middleware.config import ROOT_DIR
from flask import Blueprint, render_template, request, session, redirect
import json


users_page = Blueprint('users', __name__, template_folder='templates')

@users_page.route('/save', methods=['POST'])
def save():
    user_name = request.form.get('name')
    user_id = UserService.addUser(user_name)
    user = dict(
        name = user_name,
        id = user_id
    )
    session['user'] = user
    return redirect("/")

@users_page.route('/delete', methods=['POST'])
def delete():
    # UserService.deleteUser(session['user']['id'])
    session.pop('user')
    return redirect("/")


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
        print(_user)
        _users.append(_user)
    return json.dumps(_users)