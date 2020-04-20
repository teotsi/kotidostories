from flask import request, jsonify
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from kotidostories import db
from kotidostories.models import Post
from kotidostories.utils.auth_utils import get_request_data
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
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Invalid parameters!'}), 400
    return jsonify({"post": serialize(post), "message": "Put post successfully!"})
