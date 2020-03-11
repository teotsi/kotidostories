from flask_marshmallow.sqla import ModelSchema

from kotidostories.models import Post
from kotidostories import ma


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
