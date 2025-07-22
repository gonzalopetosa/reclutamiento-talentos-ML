from functools import wraps
from flask import request, abort
from services.Security import Security

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Security.validate_token(request.headers):
            abort(401, 'Unauthorized')
        return f(*args, **kwargs)
    return decorated
