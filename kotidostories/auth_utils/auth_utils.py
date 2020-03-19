# used for routes that require the user to be logged in
import datetime
import importlib
import uuid
from functools import wraps

from flask import jsonify, url_for
from flask_login import current_user, login_user
from flask_mail import Message

from kotidostories import bcrypt, db, mail
from kotidostories.models import User


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'You are not authorized'}), 403

    return decorated


def serialize(object):
    class_name = f'{type(object).__name__}Schema'
    cls = getattr(importlib.import_module(f'kotidostories.schemas.{class_name}'), class_name)

    return cls().dump(object)


def send_reset_email(user, frontend='http://localhost:3000/reset?'):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{frontend}token={token}
This token is going to be active until {datetime.datetime.now() + datetime.timedelta(minutes=30)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def register(username, email, password, login=True):
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
    user = User(id=str(uuid.uuid4()), username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    if login:
        login_user(user, remember=False)  # logging user in
    return jsonify({'message': 'New user created!'})
