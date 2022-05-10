from Auth import auth_required
from middleware.config import log
from services.SettingService import SettingService
from flask import request
from flask_restx import Resource, Namespace

ns = Namespace(
    'Setting', 
    path="/settings",
    description='Api setting operations',
    authorizations={
        'BearerAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)

@ns.route('/')
class Setting_Base(Resource):
    
    @ns.doc(params={
        'id': {'in': 'query', 'description': 'Setting id', 'type': str, 'required': False},
    })
    def get(self):
        try:
            log.info(request.args)
            if "id" in request.args:
               setting = SettingService.get_by_id(request.args["id"])
            else:
                return dict(error="need id")
            return setting
        except Exception as e:
            log.error(e)
            return dict(error=e)
    
    @ns.doc(security=["BearerAuth"])
    @ns.doc(params={
        'name': {'in': 'query', 'description': 'Setting name ', 'type': str, 'required': True},
    })
    @auth_required("BEARER")
    def post(self):
        try:
            if 'name' in request.args:
                return SettingService.addSetting(name=request.args['name'])
            else:
                return dict(error="need name")
        except Exception as e:
            log.error(e)
            return dict(error=e) 

    @ns.doc(security=["BearerAuth"])
    @ns.doc(params={
        'id': {'in': 'query', 'description': 'Setting id', 'type': str, 'required': True}
    })
    @auth_required("BEARER")
    def delete(self):
        try:
            if 'id' in request.args:
                return SettingService.delete_setting(id=request.args['id'])
            else:
                return dict(error="need id")
        except Exception as e:
            log.error(e)
            return dict(error=e) 


@ns.route('/all')
class Setting_List(Resource):
    
    @ns.doc(security=["BearerAuth"])
    @auth_required("BEARER")
    def get(self):
        try:
            return SettingService.getAll()
        except Exception as e:
            log.error(e)
            return dict(error=e)


@ns.route('/connect_site')
class Setting_Site_connect(Resource):
    
    @ns.doc(security=["BearerAuth"])
    @ns.doc(params={
        'site_id': {'in': 'query', 'description': 'Site id', 'type': str, 'required': True},
        'setting_id': {'in': 'query', 'description': 'Setting id', 'type': str, 'required': True},
        'value': {'in': 'query', 'description': 'value', 'type': str, 'required': True},
    })
    @auth_required("BEARER")
    def post(self):
        try:
            if 'site_id' in request.args and 'setting_id' in request.args and 'value' in request.args:
                return SettingService.add_value(value=request.args["value"], setting_id=request.args["setting_id"], site_id=request.args["site_id"])
            else:
                return "not enough data"
        except Exception as e:
            log.error(e)
            return dict(error=e)


    @ns.doc(security=["BearerAuth"])
    @ns.doc(params={
        'url': {'in': 'query', 'description': 'Url site: https://site.org', 'type': str, 'required': False},
        'name': {'in': 'query', 'description': 'Site name ', 'type': str, 'required': False},
        'site_id': {'in': 'query', 'description': 'Site id', 'type': str, 'required': False},
    })
    @auth_required("BEARER")
    def get(self):
        try:
            log.info(request.args)
            if "site_id" in request.args:
               setting = SettingService.get_value_settings(site_id=request.args["site_id"])
            elif "name" in request.args:
               setting = SettingService.get_value_settings(name=request.args["name"])
            elif "url" in request.args:
               setting = SettingService.get_value_settings(url=request.args["url"])
            else:
                return dict(error="need id or name or url")
            return setting
        except Exception as e:
            log.error(e)
            return dict(error=e)