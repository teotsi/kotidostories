import importlib
import uuid


def create_id():
    return str(uuid.uuid4())


def serialize(object):
    class_name = f'{type(object).__name__}Schema'
    cls = getattr(importlib.import_module(f'kotidostories.schemas.{class_name}'), class_name)

    return cls().dump(object)