from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models import Comment


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Comment
