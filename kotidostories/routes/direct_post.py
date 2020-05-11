from flask import Blueprint, jsonify

from kotidostories.models import Post
from kotidostories.utils.auth_utils import auth_required
from kotidostories.utils.general_utils import serialize
from kotidostories.utils.post_utils import save_post, react
from kotidostories.utils.post_utils.post_utils import delete_react

direct_post_bp = Blueprint('direct_post_bp', __name__, url_prefix='/post/')


@direct_post_bp.route('/')
def get_all_posts():
    posts = Post.query.all()
    return jsonify(serialize(posts))


@direct_post_bp.route('/<string:id>/')
def get_post(id=None):
    post = Post.query.filter_by(id=id).first()
    return jsonify(serialize(post))


@direct_post_bp.route('/', methods=["POST"])
@auth_required()
def upload_post():
    return save_post()


# TODO
# decide if REST endpoints that do require username/id should be here

@direct_post_bp.route('/<string:id>/reaction/', methods=['POST'])
@auth_required()
def react_to_post(id=None):
    return react(id)


@direct_post_bp.route('/<string:id>/reaction/<string:reaction_id>/', methods=['DELETE'])
@auth_required()
def delete_reaction(id=None, reaction_id=None):
    return delete_react(reaction_id)
