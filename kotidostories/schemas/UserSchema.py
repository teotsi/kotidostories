import base64

from marshmallow import pre_load, pre_dump, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from kotidostories.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = User

    posts = Nested('PostSchema', many=True)
    comments = Nested('CommentSchema', many=True, exclude=['user'])
    reactions = Nested('ReactionSchema', many=True, exclude=['user'])
    transactions = Nested('TransactionSchema', many=True, exclude=['user', 'company_amount'])
