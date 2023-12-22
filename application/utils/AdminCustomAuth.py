from functools import wraps
from flask import abort
from flask import render_template
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != "admin":
            return render_template('error/404.html', title='404 Not Found'), 404
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != "staff":
            return render_template('error/404.html', title='404 Not Found'), 404
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != "user":
            return render_template('error/404.html', title='404 Not Found'), 404
        return f(*args, **kwargs)
    return decorated_function