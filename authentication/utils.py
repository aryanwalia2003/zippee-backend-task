import jwt
import datetime
from django.conf import settings
from functools import wraps
from .models import User
from core.api_utils import UnauthorizedError

def generate_token(user_id, role):
    """
    Generate a JWT token for the specified user ID and role.
    """
    payload = {
        'user_id': user_id,
        'role': role,
        "username": User.get_by_id(user_id)['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_token(token):
    """
    Decode a JWT token and retrieve the payload.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """
    Decorator to enforce authentication on view functions.
    """
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        """
        The wrapped view function that checks for a valid token.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise UnauthorizedError('Unauthorized: Missing token')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header
        payload = decode_token(token)
        
        if not payload:
            raise UnauthorizedError('Unauthorized: Invalid or expired token')
        
        request.user_id = payload['user_id']
        request.role = payload.get('role', 'user')
        return f(request, *args, **kwargs)
    return decorated_function
