import base64
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
    if 'User' in object_cls or 'Post' in object_cls:
        with open(serialized_obj['img'], "rb") as imgf:
            serialized_obj['img'] = base64.b64encode(imgf.read()).decode()
    return serialized_obj

def create_pictures_directory():
    Path("pictures/profile").mkdir(parents=True, exist_ok=True)
    Path("pictures/post").mkdir(parents=True, exist_ok=True)
