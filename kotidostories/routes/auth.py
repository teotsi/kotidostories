from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from kotidostories import bcrypt, db, q
from kotidostories.models.user import User, verify_reset_token
from kotidostories.schemas.PostSchema import PostSchema
from kotidostories.utils.auth_utils import send_reset_email, get_request_data, get_token, register_user
from kotidostories.utils.general_utils import serialize

auth_bp = Blueprint('auth_bp', __name__)
post_schema = PostSchema()


@auth_bp.route('/login/', methods=['POST'])
def log_in():
    if current_user.is_authenticated:  # if user is logged in register shouldn't be accessible
        return jsonify({'message': 'Already authenticated'}), 200

    data = get_request_data(request)
    print(data)
    email = data['email']
    password = data['password']
    remember_me = data['remember_me']
    user = User.query.filter_by(email=email).first()  # checking if user exists
    print(bcrypt.generate_password_hash(password).decode('utf-8'))
    if user and bcrypt.check_password_hash(user.password_hash, password):

        login_user(user, remember=bool(remember_me))
        return jsonify({'user': serialize(user),
                        'token': get_token(user)}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if user is logged in, register shouldn't be accessible
        return jsonify({'message': 'Already logged in'}), 403

    data = get_request_data(request)
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not (email and username and password):  # checking if necessary credentials were provided
        return jsonify({'message': 'Missing credentials'}), 403
    return register_user(username, email, password)


@auth_bp.route("/logout/")
def logout():
    logout_user()
    return jsonify({'message': 'Logged out!'})


@auth_bp.route("/resetPass/", methods=['POST'])
def request_reset_token():
    data = get_request_data(request)
    if current_user.is_authenticated:
        return jsonify({'message': 'Authenticated'}), 403
    user = verify_reset_token(data.get('token'))
    if user:
        try:
            password = data.get('form')['password']
            password_hash = bcrypt.generate_password_hash(password)
            user.password_hash = password_hash
            db.session.commit()
            return jsonify({'message': 'Valid token'})
        except (KeyError, IntegrityError) as e:
            print(e)
            db.session.rollback()
            return {'message': 'invalid parameters!'}, 400
    else:
        return jsonify({'message': 'Invalid token'}), 403


@auth_bp.route("/verifyToken/", methods=['POST'])
def verify_token():
    if current_user.is_authenticated:
        return jsonify({'message': 'Authenticated'}), 403
    data = get_request_data(request)
    token = data.get('token')
    user = verify_reset_token(token)
    if user:
        return jsonify({'status': True})
    else:
        return jsonify({'status': False}), 200


@auth_bp.route("/reset", methods=['POST'])
def reset_token():
    if current_user.is_authenticated:
        return jsonify({'message': 'Authenticated'}), 403
    data = get_request_data(request)
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        send_reset_email(user)
    return jsonify({'message': ''})


@auth_bp.route("/checkUsername/<string:username>")
def check_username(username=None):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "username is available!"})
    else:
        return jsonify({"message": "Username is unavailable"}), 401
