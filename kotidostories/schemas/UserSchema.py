from kotidostories.models import User
from kotidostories.schemas.CommentSchema import CommentSchema
from kotidostories.schemas.PostSchema import PostSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = User

    posts = Nested(PostSchema, many=True, exclude=['user'])
    comments = Nested(CommentSchema, many=True, exclude=['user'])
