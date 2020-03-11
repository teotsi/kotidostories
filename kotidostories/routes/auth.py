from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify
import uuid
from flask_login import login_user, current_user, logout_user
from kotidostories import bcrypt, db
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
        posts = [PostSchema().dump(post) for post in user.posts]
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

    login_user(user, remember=False)  # logging user in
    return jsonify({'message': 'New user created!'})


@auth_bp.route("/logout")
def logout():
    logout_user()
    return jsonify({'message': 'Logged out!'})
