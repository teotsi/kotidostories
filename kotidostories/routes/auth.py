from flask import Blueprint, render_template, request, flash
from kotidostories.models import User
auth_bp = Blueprint('login_bp', __name__)


@auth_bp.route('/login')
def log_in():
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def log_in_post():
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

    user = User.query.filter_by(email=email).first()

    if user:
        flash('There\'s already a user with this email address')
        return render_template('sign_up.html',title='Sign up')
    flash("test")
    return render_template('sign_up.html')


