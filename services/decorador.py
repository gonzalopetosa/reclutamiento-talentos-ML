from functools import wraps
from flask import request, abort
from services.Security import Security

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Security.validate_token_header(request.headers):
            abort(401, 'Unauthorized')
        return f(*args, **kwargs)
    return decorated

def token_required_cookie(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = Security.validate_token_cookie()

        if not payload:
            abort(401, 'Token inválido o expirado')
        return f(*args, **kwargs)
    return decorated