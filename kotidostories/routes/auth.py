from flask import Blueprint, render_template, request, flash, redirect, url_for
import uuid
from flask_login import login_user, current_user, logout_user
from kotidostories import bcrypt, db
from kotidostories.models import User
from kotidostories.forms import *

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:  # if user is logged in register shouldn't be accessible
        return redirect(url_for('landing_bp.landing_page'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()  # checking if user exists
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back {user.username}!', 'success')
            return redirect(url_for('landing_bp.landing_page'))
        else:
            flash('Login unsuccessful')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if user is logged in register shouldn't be accessible
        return redirect(url_for('landing_bp.landing_page'))

    form = RegistrationForm()
    if form.validate_on_submit():  # checking input
        email = form.email.data
        username = form.username.data
        password = form.password.data
        pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(id=str(uuid.uuid4()), username=username, email=email, password_hash=pass_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {form.username.data}!", 'success')
        return redirect(url_for('landing_bp.landing_page'))
    return render_template('sign_up.html', title='Register', form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing_bp.landing_page'))
