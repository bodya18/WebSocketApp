from Auth import auth_required
from middleware.config import log
from services.SiteService import SiteService
from flask import request
from flask_restx import Resource, Namespace

ns = Namespace(
    'Site', 
    path="/site",
    description='Api site operations',
    authorizations={
        'BearerAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)

@ns.route('/')
class Site_Base(Resource):
    
    @ns.doc(params={
        'url': {'in': 'query', 'description': 'Url site: https://site.org', 'type': str, 'required': False},
        'name': {'in': 'query', 'description': 'Site name ', 'type': str, 'required': False},
        'id': {'in': 'query', 'description': 'Site id', 'type': str, 'required': False},
    })
    def get(self):
        try:
            log.info(request.args)
            if "id" in request.args:
               site = SiteService.get_by_id(request.args["id"])
            elif "name" in request.args:
               site = SiteService.get_by_name(request.args["name"])
            elif "url" in request.args:
               site = SiteService.get_by_url(request.args["url"])
            else:
                return dict(error="need id or name or url")
            return site
        except Exception as e:
            log.error(e)
            return dict(error=e)
    
    @ns.doc(security=["BearerAuth"])
    @ns.doc(params={
        'url': {'in': 'query', 'description': 'Url site: https://site.org', 'type': str, 'required': True},
        'name': {'in': 'query', 'description': 'Site name ', 'type': str, 'required': True},
    })
    @auth_required("BEARER")
    def post(self):
        try:
            if 'url' in request.args and 'name' in request.args:
                return SiteService.addSite(name=request.args['name'], url=request.args['url'])
            else:
                return dict(error="need name and url")
        except Exception as e:
            log.error(e)
            return dict(error=e) 

    @ns.doc(security=["BearerAuth"])
    @ns.doc(params={
        'id': {'in': 'query', 'description': 'Site id', 'type': str, 'required': True}
    })
    @auth_required("BEARER")
    def delete(self):
        try:
            if 'id' in request.args:
                return SiteService.delete_site(id=request.args['id'])
            else:
                return dict(error="need id")
        except Exception as e:
            log.error(e)
            return dict(error=e) 


@ns.route('/all')
class Site_List(Resource):
    
    def get(self):
        try:
            return SiteService.getAll()
        except Exception as e:
            log.error(e)
            return dict(error=e)