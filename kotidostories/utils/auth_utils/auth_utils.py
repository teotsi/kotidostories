# used for routes that require the user to be logged in
from datetime import datetime, timedelta
import json
from functools import wraps

import jwt
from flask import jsonify
from flask_login import current_user, login_user
from flask_mail import Message

from kotidostories import bcrypt, db, mail
from kotidostories.models import User


def auth_required(authorization=False):
    def auth_check(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.is_authenticated:
                if authorization:
                    if current_user.username == kwargs['user']:
                        return f(*args, **kwargs)
                else:
                    return f(*args, **kwargs)
            return jsonify({'message': 'You are not authorized'}), 403

        return decorated

    return auth_check


def send_reset_email(user, frontend='http://localhost:3000/reset?'):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{frontend}token={token}
This token is going to be active until {datetime.now() + timedelta(minutes=60)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def register_user(username, email, password, login=True):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # querying db to search if email already exists
    email_exists = User.query.filter_by(email=email).first()
    if email_exists:
        return jsonify({'message': 'Email is taken!'}), 403

    # same for username
    username_exists = User.query.filter_by(username=username).first()
    if username_exists:
        return jsonify({'message': 'Username is taken!'}), 403

    # creating user and adding to database
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    if login:
        login_user(user, remember=False)  # logging user in
    return jsonify({'message': 'New user created!'})


def get_request_data(request):
    data = request.get_json()
    if not data:
        try:
            return json.loads(request.form.getlist('data')[0])
        except IndexError:
            return {}
    return data


def get_token(user):
    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        'So safe')
    return token.decode('UTF-8')