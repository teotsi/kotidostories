from flask import Blueprint, jsonify, request
from flask_login import current_user

from kotidostories import db
from kotidostories.models import Transaction, User
from kotidostories.utils.auth_utils import auth_required, get_request_data
from kotidostories.utils.general_utils import serialize

donating_bp = Blueprint('donating_bp', __name__, url_prefix='/user/<string:user>/donation/')


@donating_bp.route('/')
@auth_required(authorization=True)
def get_donations(user=None):
    donations = Transaction.query.filter_by(to_user=current_user.id).all()

    return jsonify({"donations": serialize(donations)})


@donating_bp.route('/', methods=['POST'])
@auth_required(authorization=True)
def make_donation(user=None):
    data = get_request_data(request)
    amount = data.get('amount')
    user_id = User.query.filter_by(username=user).first().id
    transaction = Transaction(to_user=user_id, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"donation": serialize(transaction)})
