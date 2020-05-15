from flask import request, jsonify
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from kotidostories import db
from kotidostories.models import Post, Reaction
from kotidostories.utils.auth_utils import get_request_data
from kotidostories.utils.es_utils import index_post, update_index
from kotidostories.utils.general_utils import save_img, serialize


def save_post():
    data = get_request_data(request)
    content = data.get('content')
    title = data.get('title')
    preview = data.get('preview')
    category = data.get('category')
    try:
        published = data.get('published')
    except KeyError:
        published = True
    try:
        post = Post(user_id=current_user.id, content=content, title=title, preview=preview, category=category,
                    published=published)
        if 'image' in request.files:
            save_img(request.files['image'], post, current_user.id, post.id)
        db.session.add(post)
        db.session.commit()
        index_post(post)
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Invalid parameters!'}), 400
    return jsonify({"post": serialize(post), "message": "Put post successfully!"})


def refresh_post(id=None):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.user_id == current_user.id:
        data = get_request_data(request)
        if 'image' in request.files:
            save_img(request.files['image'], post, current_user.id, id)
        for key, value in data.items():
            post.update(key, value)
        db.session.commit()
        update_index(post)
        return jsonify({"message": 'Updated post!'})
    else:
        return jsonify({"message": 'unauthorized!'}), 403


def react(id=None):
    post = Post.query.filter_by(id=id).first_or_404()

    from_author = post.user_id == current_user.id
    data = request.get_json()
    reaction_type = data.get('type')
    reaction_exists = next((reaction for reaction in post.reactions.all()
                            if reaction.user_id == current_user.id), None)

    if reaction_exists:
        reaction = reaction_exists
        reaction.type = reaction_type
    else:
        reaction = Reaction(user_id=current_user.id, post_id=id, type=reaction_type,
                            from_author=from_author)
        post.reactions.append(reaction)
    db.session.commit()
    return jsonify({'message': 'react successful',
                    'reaction': serialize(reaction)})


def delete_react(id=None):
    reaction = Reaction.query.filter_by(id=id).first_or_404()
    if current_user.id == reaction.user_id:
        db.session.delete(reaction)
        db.session.commit()
        return jsonify({'message': 'deleted reaction'})
    return jsonify({'message': 'who are you?'}), 403
