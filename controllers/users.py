import datetime
import uuid
from Auth import auth_required
from middleware.config import ROOT_DIR, STATUS_LIST, log
from services.UserService import UserService
from flask import request, send_file
import os
from flask_restx import Resource, Namespace

ns = Namespace(
    'User', 
    path="/api",
    description='Api user operations',
    authorizations={
        'BearerAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)


@ns.route('/users/add')
class Add_User(Resource):
    @ns.doc(params={
        'name': {'in': 'query', 'description': 'User name', 'type': str, 'required': True},
        'email': {'in': 'query', 'description': 'User email', 'type': str, 'required': True},
        'site': {'in': 'query', 'description': 'Site used by user', 'type': str, 'required': False},
    })
    def post(self):
        try:
            print(request.args)
            if len(request.args['name'])<2 or len(request.args['name'])>15:
                return {"error": "length name need min 2 and max 15"}
            user_name = request.args['name']
            user_email = request.args['email']
            user_site = request.args['site'] if 'site' in request.args else None
            user = UserService.get_by_email(user_email)
            if user is None:
                user = UserService.addUser(user_name, user_email, role="User")
                return user
            elif user.status == "Banned":
                return dict(error="User banned")
            elif user.name == user_name:
                return user.serialize()
            else: 
                return dict(error="invalid name")
        except Exception as e:
            log.error(e)
            return dict(error="need in params name and email")


@ns.route('/users/all')
@ns.doc(security=["BearerAuth"])
class Get_All(Resource):
    @ns.doc(params={
        'page': {'in': 'query', 'description': 'Current page', 'type': int, 'required': False},
        'limit': {'in': 'query', 'description': 'Limit users in page', 'type': int, 'required': False},
    })
    @auth_required("BEARER")
    def get(self):
        log.info(request.args)
        users = UserService.getAll()
        page = int(request.args['page']) if 'page' in request.args else 1
        limit = int(request.args['limit']) if 'limit' in request.args else 100
        length = len(users)
        users=[user.serialize() for user in users]
        users = sorted(users, key=lambda d: d["last_message"]["date"], reverse=True) 
        users = users[page*limit-limit:page*limit]
        users = dict(
            users=users,
            length=length
        )
        return users

@ns.route('/users/all/status')
@ns.doc(security=["BearerAuth"])
class GetByStatus(Resource):
    @ns.doc(params={
        # 'page': {'in': 'query', 'description': 'Current page', 'type': int, 'required': False},
        # 'limit': {'in': 'query', 'description': 'Limit users in page', 'type': int, 'required': False},
        'status': {'in': 'query', 'description': 'User status', 'type': str, 'required': True},
    })
    @auth_required("BEARER")
    def get(self):
        try:
            log.info(request.args)
            status = request.args['status']
            if status in STATUS_LIST:
                users = UserService.getStatus(status)
                # page = int(request.args['page']) if 'page' in request.args else 1
                # limit = int(request.args['limit']) if 'limit' in request.args else 100
                users=[user.serialize() for user in users]
                users = sorted(users, key=lambda d: d["last_message"]["date"], reverse=True)
                length = len(users)
                # users = users[page*limit-limit:page*limit]
                users = dict(
                    users=users,
                    length=length
                )
                return users
            else:
                return dict(error="Status not valid")
        except Exception as e:
            log.error(e)
            return dict(error="need in params status")


@ns.route('/users/messages')
@ns.doc(security=["BearerAuth"])
class GetAllMessages(Resource):
    @ns.doc(params={
        'user_id': {'in': 'query', 'description': 'User identificator', 'type': int, 'required': True},
    })
    @auth_required("BEARER")
    def get(self):
        try:
            log.info(request.args)
            user_id = request.args['user_id']
            messages = UserService.get_messages_by_userId(user_id)
            return [msg.serialize() for msg in messages]
        except Exception as e:
            log.error(e)
            return dict(error="need in params user_id")


@ns.route('/users/new/status')
@ns.doc(security=["BearerAuth"])
class UpdateUserStatus(Resource):
    @ns.doc(params={
        'id': {'in': 'query', 'description': 'User identificator', 'type': int, 'required': True},
        'status': {'in': 'query', 'description': 'User status', 'type': str, 'required': True},
    })
    @auth_required("BEARER")
    def post(self):
        try:
            log.info(request.args)
            status = request.args['status']
            id = request.args['id']
            if status in STATUS_LIST:
                user = UserService.update_status(status, id)
                return user
            else:
                return dict(error="Status not valid")
        except Exception as e:
            log.error(e)
            return dict(error="need in params status, id")


from werkzeug.datastructures import FileStorage
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@ns.route('/file/upload')
@ns.expect(upload_parser)
class FileUpload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        if 'file' not in args:
            log.warning("No file")
            return dict(error="No file")
        file = args['file']
        if file.filename == '':
            log.warning('NO selected file')
            return dict(error='NO selected file')
        try:
            file_type = file.filename.rsplit('.', 1)[1].lower()
        except:
            file_type = ''
        filename = uuid.uuid4().hex
        try:
            os.makedirs(f"{ROOT_DIR}/files")
        finally:
            file.save(os.path.join(f"./files/", f"{filename}{'.'+file_type if file_type!='' else ''}"))
            return f"{filename}{'.'+file_type if file_type!='' else ''}"


@ns.route('/file/<string:file_name>')
class GetFile(Resource):
    def get(self, file_name):
        try:
            return send_file(f"./files/{file_name}")
        except:
            return "file doesn't exist"