from flask import Blueprint, render_template, request, flash
import uuid

from kotidostories import bcrypt, db
from kotidostories.models import User

auth_bp = Blueprint('login_bp', __name__)


@auth_bp.route('/login')
def log_in():
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def log_in_post():
    username = request.form.get('username')
    password = request.form.get('password')
    return 1


@auth_bp.route('/register')
def register():
    return render_template('sign_up.html')


@auth_bp.route('/register', methods=['POST'])
def register_post():
    # extracting data from request
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('There\'s already a user with this email address')
        return render_template('sign_up.html', title='Sign up')
    new_user = User(id=str(uuid.uuid4()),email=email, username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flash('Your account has been created!')

    return render_template('sign_up.html', title='Sign up')
