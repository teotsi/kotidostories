from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
