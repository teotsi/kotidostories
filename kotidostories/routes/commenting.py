from flask import Blueprint, jsonify, request
from flask_login import current_user

from kotidostories import db
from kotidostories.models import Comment, Post, User
from kotidostories.utils.auth_utils import auth_required, get_request_data
from kotidostories.utils.general_utils import serialize

commenting_bp = Blueprint('commenting_bp', __name__, url_prefix='/user/<string:user>/posts/<string:post_id>/comments/')


# TODO

@commenting_bp.route('/')
def get_comments(user=None, post_id=None):
    post = Post.query.filter_by(id=post_id).first()
    return jsonify({'comments': serialize(post.comments)})


@commenting_bp.route('/', methods=['POST'])
@auth_required()
def post_comment(user=None, post_id=None):
    data = get_request_data(request)
    user_data = User.query.filter_by(username=user).first_or_404()
    user_posts = user_data.posts
    for post in user_posts:
        if post.id == post_id:
            content = data.get('content')
            user_id = current_user.id
            from_author = user_id == post.user_id
            comment = Comment(user_id=user_id, post_id=post_id, content=content,
                              from_author=from_author)
            db.session.add(comment)
            db.session.commit()
            return jsonify({'comment': serialize(comment)})
    return jsonify({'message': 'invalid'}), 403


@commenting_bp.route('/<string:comment_id>', methods=['PATCH'])
@auth_required()
def edit_comment(user=None, post_id=None, comment_id=None):
    data = get_request_data(request)
    user_data = User.query.filter_by(username=user).first_or_404()
    user_posts = user_data.posts
    for post in user_posts:
        if post.id == post_id:
            for comment in post.comments:
                if comment.id == comment_id:
                    for key, value in data.items():
                        comment.update(key, value)
                        db.session.commit()
                        return jsonify({'message': 'Edited comment'})
            return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Invalid'}), 403
