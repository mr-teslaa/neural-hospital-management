# decorators.py
from functools import wraps
from flask import abort, current_app
from application.models import User
from flask_login import current_user

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                # Redirect to login or return a response indicating unauthenticated access
                abort(401)  # Unauthorized

            if current_user.role not in required_roles:
                # Redirect to an error page or return a response indicating access forbidden
                abort(403)  # Forbidden

            return func(*args, **kwargs)

        return wrapper

    return decorator
