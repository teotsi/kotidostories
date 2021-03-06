import importlib
import uuid
from collections.abc import Iterable
from pathlib import Path, PurePosixPath


def create_id():
    return str(uuid.uuid4())


def serialize(object):
    object_cls = type(object).__name__  # getting object' class nam, e.g User, Post
    class_name = f'{object_cls}Schema'  # appending 'Schema' suffix to create Marshmallow class name

    if isinstance(object, Iterable):  # lists cannot be dumped automatically
        return [serialize(item) for item in object]  # so we use recursion on each item of said list

    cls = getattr(importlib.import_module(f'kotidostories.schemas.{class_name}'),
                  class_name)  # getting a reference to the class

    serialized_obj = cls().dump(object)
    return serialized_obj


def create_pictures_directory(user_id="", post_id=""):
    Path(f"pictures/user/{user_id}").mkdir(parents=True, exist_ok=True)
    Path(f"pictures/post/{user_id}/{post_id}").mkdir(parents=True, exist_ok=True)


def save_img(image, obj, user_id, post_id=''):
    if image.filename == '':
        return
    image_extension = image.filename.split('.')[-1]
    image_name = f'{obj.id}.{image_extension}'
    create_pictures_directory(user_id=user_id, post_id=post_id)
    object_cls = obj.__tablename__
    obj.img = str(PurePosixPath('pictures') / object_cls / user_id / post_id / image_name)
    image.save(obj.img)
