from operator import itemgetter

from flask import Blueprint, jsonify, request

from kotidostories.models import Post
from kotidostories.utils.general_utils import serialize

discover_bp = Blueprint('discover_bp', __name__, url_prefix='/discover')


@discover_bp.route('/')
def discover_stories():
    posts = Post.query.all()
    posts = [serialize(post) for post in posts if post.published]
    category = request.args.get('category')
    if category:
        posts = [post for post in posts if post['category'] == category]
    sort = request.args.get('sort')
    posts = sorted(posts, key=itemgetter('date'), reverse=sort == 'new')
    return jsonify({'posts': posts})
