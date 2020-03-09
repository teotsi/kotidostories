from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify
import uuid
from flask_login import login_user, current_user, logout_user
from kotidostories import bcrypt, db
from kotidostories.models import User
from kotidostories.forms import *

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:  # if user is logged in register shouldn't be accessible
        return jsonify({'message': 'Already authenticated'}), 401

    data = request.get_json()
    email = data['email']
    password = data['password']
    remember_me = data['remember_me']
    user = User.query.filter_by(email=email).first()  # checking if user exists
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user, remember=bool(remember_me))
        return jsonify({'message': 'Authenticated!'}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if user is logged in register shouldn't be accessible
        return jsonify({'message': 'Already logged in'}), 403

    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not (email and username and password):
        return jsonify({'message': 'Missing credentials'}), 403
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(id=str(uuid.uuid4()), username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


@auth_bp.route("/logout")
def logout():
    logout_user()
    return jsonify({'message': 'Logged out!'})
