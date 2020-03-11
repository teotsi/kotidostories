# used for routes that require the user to be logged in
from functools import wraps

from flask import jsonify
from flask_login import current_user


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'You are not authorized'}), 403

    return decorated
