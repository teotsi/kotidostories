import uuid

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_login import current_user

from kotidostories import db
from kotidostories.auth_utils import auth_required, serialize
from kotidostories.models import User, Post, Comment
from kotidostories.schemas.PostSchema import PostSchema

post_schema = PostSchema()
posting_bp = Blueprint('posting_bp', __name__, url_prefix='/user/<string:user>/')


@posting_bp.route('posts/', methods=['GET'])
def get_posts(user=None):
    user = User.query.filter_by(username=user).first()
    if user:
        posts = [serialize(post) for post in user.posts]
        return jsonify({'posts': posts})
    else:
        return jsonify({'message': 'No such user'}), 403


@posting_bp.route('posts/', methods=['POST'])
@auth_required
@cross_origin()
def upload_post(user=None):
    if current_user.username == user:
        data = request.get_json()
        content = data.get('content')
        title = data.get('title')
        preview = data.get('preview')
        post = Post(id=str(uuid.uuid4()), user_id=current_user.id, content=content, title=title, preview=preview)
        db.session.add(post)
        db.session.commit()
        return jsonify({"post": serialize(post), "message": "Put post successfully!"}),{'Access-Control-Allow-Origin': '*'}
    return jsonify({'message': 'No access'}), 403,{'Access-Control-Allow-Origin': '*'}


@posting_bp.route('posts/<string:post_id>', methods=['DELETE'])
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


@posting_bp.route('posts/<string:post_id>', methods=['PATCH'])
@auth_required
def update_post(user=None, post_id=None):
    if current_user.username == user:
        post = Post.query.filter_by(id=post_id).first_or_404()
        data = request.get_json()
        for key, value in data.items():
            post.update(key, value)
        db.session.commit()
        return jsonify({"message": 'Updated post!'})
    return jsonify({'message': 'You are not the author!'}), 403


@posting_bp.route('/')
def get_user(user=None):
    user_info = User.query.filter_by(username=user).first_or_404()
    return jsonify({"user": serialize(user_info)})


@posting_bp.route('/comments')
def get_comments(user=None):
    comments = User.query.filter_by(username=user).join(Comment).all()
    print(comments)
    return jsonify({'comments': comments})
