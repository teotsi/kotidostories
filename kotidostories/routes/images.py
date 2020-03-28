import os

from flask import Blueprint, send_from_directory

images_bp = Blueprint('images_bp', __name__, url_prefix='/pictures/')


@images_bp.route('profile/<string:user_id>/<string:img>')
def get_profile_image(user_id=None, img=None):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, os.environ['PIC_FLASK'], 'pictures', 'profile', user_id), img)


@images_bp.route('/post/<string:user_id>/<string:post_id>/<string:img>')
def get_post_image(user_id=None, post_id=None, img=None):
    root_dir = os.path.dirname(os.getcwd())
    print(os.environ['PIC_FLASK'])
    return send_from_directory(os.path.join(root_dir, os.environ['PIC_FLASK'], 'pictures', 'post', user_id, post_id),
                               img)
