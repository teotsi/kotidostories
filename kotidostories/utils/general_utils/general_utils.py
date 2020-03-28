import importlib
import uuid
from pathlib import Path


def create_id():
    return str(uuid.uuid4())


def serialize(object):
    object_cls = type(object).__name__
    class_name = f'{object_cls}Schema'
    cls = getattr(importlib.import_module(f'kotidostories.schemas.{class_name}'), class_name)
    serialized_obj = cls().dump(object)
    return serialized_obj


def create_pictures_directory(user_id="", post_id=""):
    Path("pictures/profile").joinpath(user_id).mkdir(parents=True, exist_ok=True)
    Path("pictures/post").joinpath(user_id, post_id).mkdir(parents=True, exist_ok=True)


def save_img(image):
    pass
