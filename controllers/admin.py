from middleware.config import log
from services.UserService import UserService
from flask import request
import bcrypt
from flask_restx import Resource, Namespace

ns = Namespace(
    'Admin', 
    path="/admin",
    description='Api admin operations'
)

@ns.route('/login')
class Login(Resource):
    @ns.doc(params={
        'name': {'in': 'query', 'description': 'Admin name', 'type': str, 'required': True},
        'password': {'in': 'query', 'description': 'Admin password', 'type': str, 'required': True},
    })
    def put(self):
        try:
            log.info(request.args)
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
                return dict(auth=False, error="invalid name or password")
        except Exception as e:
            log.error(e)
            return dict(error="need in params name and password")

# @ns.route('/login')
# class Add_admin(Resource):
#     def get(self):
#         password = "sHq1U4oua8yZYAFqCFi4mRfmxB3vjp1sjvfAuxVM8hPywkHXG1QD77oguhwXMMPojF1mzy"
#         hashed_pass = bcrypt.hashpw(password.encode('UTF_8'), bcrypt.gensalt())
#         UserService.add_admin(name="admin", password=hashed_pass, role="Admin")
#         return "add"