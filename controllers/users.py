import uuid
from Auth import auth_required
from middleware.config import ROOT_DIR, STATUS_LIST, log
from services.UserService import UserService
from flask import Blueprint, request
import json
import os

api_bp = Blueprint('api', __name__, template_folder='templates')

@api_bp.route('/users/add', methods=['POST'])
def add_user():
    try:
        log.info(request.args)
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
        log.error(e)
        return dict(error="need in params name and email")

@api_bp.route('/users/all', methods=['GET'])
@auth_required("BEARER")
def get_all():
    log.info(request.args)
    users = UserService.getAll()
    page = int(request.args['page']) if 'page' in request.args else 1
    limit = int(request.args['limit']) if 'limit' in request.args else 100
    length = len(users)
    users = users[page*limit-limit:page*limit]
    users = dict(
        users=[user.serialize() for user in users],
        length=length
    )
    return users

@api_bp.route('/users/all/status', methods=['GET'])
@auth_required("BEARER")
def get_by_status():
    try:
        log.info(request.args)
        status = request.args['status']
        if status in STATUS_LIST:
            users = UserService.getStatus(status)
            page = int(request.args['page']) if 'page' in request.args else 1
            limit = int(request.args['limit']) if 'limit' in request.args else 100
            length = len(users)
            users = users[page*limit-limit:page*limit]
            users = dict(
                users=[user.serialize() for user in users],
                length=length
            )
            return users
        else:
            return dict(error="Status not valid")
    except Exception as e:
        log.error(e)
        return dict(error="need in params status")


@api_bp.route('/users/messages', methods=['GET'])
@auth_required("BEARER")
def get_all_msg():
    try:
        log.info(request.args)
        user_id = request.args['user_id']
        messages = UserService.get_messages_by_userId(user_id)
        return json.dumps([msg.serialize() for msg in messages])
    except Exception as e:
        log.error(e)
        return dict(error="need in params user_id")


@api_bp.route('/users/new/status', methods=['POST'])
@auth_required("BEARER")
def update_status():
    try:
        log.info(request.args)
        status = request.args['status']
        id = request.args['id']
        user = UserService.update_status(status, id)
        return user
    except Exception as e:
        log.error(e)
        return dict(error="need in params status, id")


@api_bp.route('/users/file/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        log.warning("No file")
        return dict(error="No file")
    file = request.files['file']
    if file.filename == '':
        log.warning('NO selected file')
        return dict(error='NO selected file')
    try:
        file_type = file.filename.rsplit('.', 1)[1].lower()
    except:
        file_type = ''
    filename = uuid.uuid4().hex
    first_uuid = filename[:4]
    second_uuid = filename[4:8]
    try:
        os.makedirs(f"{ROOT_DIR}/files/{first_uuid}/{second_uuid}")
    except Exception as e:
        log.error(e)
    finally:
        file.save(os.path.join(f"./files/{first_uuid}/{second_uuid}", f"{filename}{'.'+file_type if file_type!='' else ''}"))
        return f"/files/{first_uuid}/{second_uuid}/{filename}{'.'+file_type if file_type!='' else ''}"
