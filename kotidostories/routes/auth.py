from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user

from kotidostories import bcrypt
from kotidostories.auth_utils import serialize, auth_utils
from kotidostories.models import User
from kotidostories.schemas.PostSchema import PostSchema

auth_bp = Blueprint('auth_bp', __name__)
post_schema = PostSchema()


@auth_bp.route('/login', methods=['POST'])
def log_in():
    if current_user.is_authenticated:  # if user is logged in register shouldn't be accessible
        return jsonify({'message': 'Already authenticated'}), 200

    data = request.get_json()
    email = data['email']
    password = data['password']
    remember_me = data['remember_me']
    user = User.query.filter_by(email=email).first()  # checking if user exists
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user, remember=bool(remember_me))
        posts = [serialize(post) for post in user.posts]
        return jsonify({'posts': posts}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if user is logged in, register shouldn't be accessible
        return jsonify({'message': 'Already logged in'}), 403

    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not (email and username and password):  # checking if necessary credentials were provided
        return jsonify({'message': 'Missing credentials'}), 403
    return auth_utils.register(username, email, password)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return jsonify({'message': 'Logged out!'})
