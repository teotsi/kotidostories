from flask import Blueprint, jsonify

from kotidostories.models import Post
from kotidostories.utils.general_utils import serialize

direct_post_bp = Blueprint('direct_post_bp', __name__, url_prefix='/post/')


@direct_post_bp.route('/')
def get_all_posts():
    posts = Post.query.all()
    return jsonify(serialize(posts))


@direct_post_bp.route('/<string:id>')
def get_post():
    post = Post.query.filter_by(id=id).first_or_404()
    return jsonify(serialize(post))

# TODO
# decide if REST endpoints that do require username/id should be here
