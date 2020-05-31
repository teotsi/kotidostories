from flask import Blueprint, request

from kotidostories.utils.es_utils import get_suggestion

suggest_bp = Blueprint('suggest_bp', __name__)


@suggest_bp.route('/suggest/')
def get_suggestions():
    post_suggestion = request.args.get('pid')
    if post_suggestion:
        return get_suggestion(id=post_suggestion)
    query = request.args.get('q', default='', type=str)
    return get_suggestion(query)
