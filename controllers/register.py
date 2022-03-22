from services.UserService import UserService
from middleware.config import ROOT_DIR
from flask import Blueprint

register_page = Blueprint('register', __name__, template_folder='templates')

@register_page.route('/register', methods=['GET'])
def gen():
    # UserService.addUser('Jhon')
    print(UserService.getAll())
    return ROOT_DIR