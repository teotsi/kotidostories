from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models import Post


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Post
