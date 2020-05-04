from flask import Blueprint, jsonify

from kotidostories.models import User

direct_user_bp = Blueprint('direct_user_bp', __name__)


@direct_user_bp.route('/user/')
def get_usernames():
    users = User.query.with_entities(User.username).all()
    users = [user[0] for user in users]
    return jsonify({"users": users})
