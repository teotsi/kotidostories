from flask import Blueprint, jsonify
from flask import request

from kotidostories import db
from kotidostories.models import Post, Reaction
from kotidostories.utils.auth_utils import auth_required
from kotidostories.utils.general_utils import serialize
from kotidostories.utils.post_utils import react
from kotidostories.utils.post_utils.post_utils import delete_react

reacting_bp = Blueprint('reacting_bp', __name__, url_prefix='/user/<string:user>/posts/<string:post_id>/reaction')


@reacting_bp.route('/<string:reaction_id>')
def get_reaction(user=None, post_id=None, reaction_id=None):
    post = Post.query.filter_by(id=post_id).first_or_404()
    reaction = post.reactions.filter_by(id=reaction_id).first_or_404()
    return jsonify({"reaction": serialize(reaction)})


@reacting_bp.route('/', methods=['GET'])
@auth_required()
def get_post_reactions(user=None, post_id=None):
    post = Post.query.filter_by(id=post_id).first_or_404()
    reactions = post.reactions.all()
    return jsonify({"reactions": serialize(reactions)})


@reacting_bp.route('/', methods=['POST'])
@auth_required()
def react_to_post(user=None, post_id=None):
    return react(post_id)


@reacting_bp.route('/<string:reaction_id>', methods=['DELETE'])
@auth_required(authorization=True)
def delete_reaction(user=None, post_id=None, reaction_id=None):
    return delete_react(reaction_id)


@reacting_bp.route('/<string:reaction_id>', methods=['PUT'])
@auth_required(authorization=True)
def update_reaction(user=None, post_id=None, reaction_id=None):
    reaction = Reaction.query.filter_by(id=reaction_id).first_or_404()
    new_type = request.get_json().get('type')
    reaction.type = new_type
    db.session.commit()
    return jsonify({'message': 'updated reaction'})
