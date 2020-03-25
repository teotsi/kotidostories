import uuid

from flask import Blueprint, jsonify, request
from flask_login import current_user

from kotidostories import db
from kotidostories.auth_utils import auth_required, serialize
from kotidostories.models import User, Post, Comment

posting_bp = Blueprint('posting_bp', __name__, url_prefix='/user/<string:user>/')


@posting_bp.route('posts/', methods=['GET'])
def get_posts(user=None):
    user = User.query.filter_by(username=user).first_or_404()
    filter = request.args.get('filter')
    if filter == 'following':
        posts = [serialize(post) for followee in user.following for post in followee.posts if post.published]
    else:
        posts = [serialize(post) for post in user.posts if post.published]
    return jsonify({'posts': posts})


@posting_bp.route('posts/', methods=['POST'])
@auth_required(authorization=True)
def upload_post(user=None):
    print("yooo upload")
    data = request.get_json()
    content = data.get('content')
    title = data.get('title')
    preview = data.get('preview')
    post = Post(id=str(uuid.uuid4()), user_id=current_user.id, content=content, title=title, preview=preview)
    db.session.add(post)
    db.session.commit()
    return jsonify({"post": serialize(post), "message": "Put post successfully!"})


@posting_bp.route('posts/<string:post_id>', methods=['DELETE'])
@auth_required(authorization=True)  # users shouldn't be able to delete posts that they haven't authored
def delete_post(user=None, post_id=None):
    post = Post.query.filter_by(id=post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})


@posting_bp.route('posts/<string:post_id>', methods=['PATCH'])
@auth_required(authorization=True)
def update_post(user=None, post_id=None):
    post = Post.query.filter_by(id=post_id).first_or_404()
    data = request.get_json()
    for key, value in data.items():
        post.update(key, value)
    db.session.commit()
    return jsonify({"message": 'Updated post!'})


@posting_bp.route('/')
def get_user(user=None):
    if user == 'me':
        if current_user.is_authenticated:
            return jsonify({'user': serialize(current_user._get_current_object())})
        else:
            return jsonify({'message': 'You need to be logged in'}), 403

    user_info = User.query.filter_by(username=user).first_or_404()
    return jsonify({"user": serialize(user_info)})


@posting_bp.route('/comments')
def get_comments(user=None):
    comments = User.query.filter_by(username=user).join(Comment).all()
    print(comments)
    return jsonify({'comments': comments})


@posting_bp.route('/follow', methods=['GET'])
@auth_required()
def follow_user(user=None):
    if current_user.username == user:
        return jsonify({"message": "Can't follow yourself man"})
    user = User.query.filter_by(username=user).first_or_404()
    user.followers.append(current_user._get_current_object())
    db.session.commit()
    return jsonify({"message": "Follow successful"})


@posting_bp.route('/follow', methods=['DELETE'])
@auth_required()
def unfollow_user(user=None):
    if current_user.username == user:
        return jsonify({"message": "Can't unfollow yourself man"})
    user = User.query.filter_by(username=user).first_or_404()
    try:
        user.followers.remove(current_user._get_current_object())
        db.session.commit()
    except ValueError:
        return jsonify({'message': 'No follow in the first place'})
    return jsonify({"message": "Unfollow successful"})

