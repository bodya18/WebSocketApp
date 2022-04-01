from services.ChatService import ChatService
from services.UserService import UserService
from middleware.config import ROOT_DIR
from flask import Blueprint, render_template, request, session, redirect
import json


users_page = Blueprint('users', __name__, template_folder='templates')

@users_page.route('/add', methods=['POST'])
def add_user():
    user_name = request.args['name']
    user_email = request.args['email']
    user_id = UserService.addUser(user_name, user_email, role="User")
    id = dict(user_id=user_id)
    return id


@users_page.route('/api/all', methods=['GET'])
def get_all():
    users = UserService.getAll()
    return json.dumps([user.serialize() for user in users])