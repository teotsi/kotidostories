from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = User
