from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from kotidostories.models import Post


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Post

    comments = Nested('CommentSchema', many=True, exclude=['post'])
    reactions = Nested('ReactionSchema', many=True, exclude=['post'])
    user = Nested("UserSchema", only=['username', 'img'])
