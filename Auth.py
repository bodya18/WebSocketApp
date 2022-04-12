from flask import request
from middleware.config import BEARER_TOKEN, log

def auth_required(auth_type):
    def dec(handler):
        def wrapper(*args, **kwargs):
            if auth_type == "BEARER":
                auth = request.headers.get("Authorization")

                if auth is None or auth[:6] != 'Bearer':
                    log.error("Need Bearer auth")
                    return dict(error = "Need Bearer auth")
                    
                if auth[7:] == BEARER_TOKEN:
                    return handler(*args, **kwargs)
                else:
                    log.error("Invalid Bearer token")
                    return dict(error = "Invalid token")
        wrapper.__name__ = handler.__name__
        return wrapper

    return dec


