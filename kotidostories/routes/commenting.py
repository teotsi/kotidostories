import uuid

from flask import Blueprint, jsonify, request
from flask_login import current_user

from kotidostories import db
from kotidostories.auth_utils import auth_required, serialize
from kotidostories.models import Comment, Post, User

commenting_bp = Blueprint('commenting_bp', __name__, url_prefix='/user/<string:user>/posts/<string:post_id>/comments/')


# TODO

@commenting_bp.route('/')
def get_comments(user=None, post_id=None):
    comments = Post.query.filter_by(id=post_id).join(Comment).all()
    print(comments)
    return jsonify({'comments': comments})


@commenting_bp.route('/', methods=['POST'])
@auth_required()
def post_comment(user=None, post_id=None):
    data = request.get_json()
    user_data = User.query.filter_by(username=user).first_or_404()
    user_posts = user_data.posts
    if any(post.id == post_id for post in user_posts):
        content = data.get('content')
        user_id = current_user.id
        comment = Comment(id=str(uuid.uuid4()), user_id=user_id, post_id=post_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'comment': serialize(comment)})
    return jsonify({'message': 'invalid'}), 403


@commenting_bp.route('/', methods=['PATCH'])
def edit_comment(user=None, post_id=None):
    data = request.get_json()
    user_data = User.query.filter_by(username=user).first_or_404()
    user_posts = user_data.posts
    if any(post.id == post_id for post in user_posts):
        comment_id = data.get('id')
        comment = Comment.query.filter_by(id=comment_id).first_or_404()
        for key, value in data.items():
            comment.update(key, value)
        db.session.commit()
        return jsonify({'message': 'Edited comment'})
    return jsonify({'message': 'Invalid'}), 403

