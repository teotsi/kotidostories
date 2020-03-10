from flask import Blueprint, render_template, jsonify

landing_bp = Blueprint('landing_bp', __name__)


@landing_bp.route('/')
def landing_page():
    return jsonify({'message':'up!'})
