from services.UserService import UserService
from flask import Blueprint, request
import json
import bcrypt

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['PUT'])
def login():
    user_name = request.args['name']
    user_pass = request.args['password']
    admin = UserService.get_admin(user_name, role="Admin")
    admin_pass = admin.password
    if admin_pass == bcrypt.hashpw(user_pass.encode('UTF_8'), admin_pass.encode('UTF_8')).decode():
        return dict(
            auth=True,
            user=admin.serialize()
        )
    else:
        return dict(auth=False)


# @admin_bp.route('/login', methods=['GET'])
# def add_admin():
#     password = "sHq1U4oua8yZYAFqCFi4mRfmxB3vjp1sjvfAuxVM8hPywkHXG1QD77oguhwXMMPojF1mzy"
#     hashed_pass = bcrypt.hashpw(password.encode('UTF_8'), bcrypt.gensalt())
#     UserService.add_admin(name="admin", password=hashed_pass, role="Admin")
#     return "add"