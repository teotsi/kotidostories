from kotidostories.models import Post
from kotidostories.schemas.CommentSchema import CommentSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Post

    comments = Nested(CommentSchema, many=True)
