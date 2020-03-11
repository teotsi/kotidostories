import uuid

from flask import Blueprint, jsonify, request
from flask_login import current_user
from functools import wraps
from kotidostories import db
from kotidostories.auth_utils import auth_required
from kotidostories.models import User, Post
from kotidostories.schemas.PostSchema import PostSchema

post_schema = PostSchema()
posting_bp = Blueprint('posting_bp', __name__, url_prefix='/user/')


@posting_bp.route('<string:user>/posts', methods=['GET'])
def get_posts(user=None):
    user = User.query.filter_by(username=user).first()
    if user:
        posts = [post_schema.dump(post) for post in user.posts]
        return jsonify({'posts': posts})
    else:
        return jsonify({'message': 'No such user'}), 403


@posting_bp.route('<string:user>/posts', methods=['PUT'])
@auth_required
def upload_post(user=None):
    if current_user.username == user:
        data = request.get_json()
        content = data.get('content')
        title = data.get('title')
        post = Post(id=str(uuid.uuid4()), user_id=current_user.id, content=content, title=title)
        db.session.add(post)
        db.session.commit()
        return jsonify({"post": post_schema.dump(post), "message": "Put post successfully!"})
    return jsonify({'message': 'No access'}), 403


@posting_bp.route('<string:user>/posts/<string:post_id>', methods=['DELETE'])
@auth_required
def delete_post(user=None, post_id=None):
    message = 'You are not the author of this post'
    code = 403
    # users shouldn't be able to delete posts that they haven't authored
    if current_user.username == user:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'message': 'Post deleted'})
        else:
            message = 'Post doesn\'t exist!'
            code = 404
    return jsonify({'message': message}), code


@posting_bp.route('<string:user>/posts/<string:post_id>', methods=['PATCH'])
@auth_required
def update_post(user=None, post_id=None):
    if current_user.username == user:
        post = Post.query.filter_by(id=post_id).first_or_404()
        data = request.get_json()
        new_title = data.get('title')
        new_content = data.get('content')
        if new_title:
            post.title = new_title
        if new_content:
            post.content = new_content
        db.session.commit()
        return jsonify({"message": 'Updated post!'})
    return jsonify({'message': 'You are not the author!'}), 403
