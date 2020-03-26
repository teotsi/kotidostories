from flask import Blueprint, jsonify
from flask import request
from flask_login import current_user

from kotidostories import db
from kotidostories.models import Post, Reaction
from kotidostories.utils.auth_utils import auth_required
from kotidostories.utils.general_utils import serialize

reacting_bp = Blueprint('reacting_bp', __name__, url_prefix='/user/<string:user>/posts/<string:post_id>/reaction')


@reacting_bp.route('/', methods=['GET'])
@auth_required()
def get_post_reactions(user=None, post_id=None):
    post = Post.query.filter_by(id=post_id).first_or_404()
    reactions = post.reactions
    return jsonify({"reactions": [serialize(reaction) for reaction in reactions]})


@reacting_bp.route('/', methods=['POST'])
@auth_required(authorization=True)
def react_to_post(user=None, post_id=None):
    post = Post.query.filter_by(id=post_id).first_or_404()

    from_author = post.user_id == current_user.id
    data = request.get_json()
    reaction_type = data.get('type')
    reaction_exists = next((reaction for reaction in post.reactions
                            if reaction.user_id == current_user.id), None)

    if reaction_exists:
        reaction = reaction_exists
        reaction.type = reaction_type
    else:
        reaction = Reaction(user_id=current_user.id, post_id=post_id, type=reaction_type,
                            from_author=from_author)
        post.reactions.append(reaction)
    db.session.commit()
    return jsonify({'message': 'react successful',
                    'reaction': serialize(reaction)})


@reacting_bp.route('/<string:reaction_id>', methods=['DELETE'])
@auth_required(authorization=True)
def delete_reaction(user=None, post_id=None, reaction_id=None):
    reaction = Reaction.query.filter_by(id=reaction_id).first_or_404()
    db.session.delete(reaction)
    db.session.commit()
    return jsonify({'message': 'deleted reaction'})


@reacting_bp.route('/<string:reaction_id>', methods=['PUT'])
@auth_required(authorization=True)
def update_reaction(user=None, post_id=None, reaction_id=None):
    reaction = Reaction.query.filter_by(id=reaction_id).first_or_404()
    new_type = request.get_json().get('type')
    reaction.type = new_type
    db.session.commit()
    return jsonify({'message': 'updated reaction'})
