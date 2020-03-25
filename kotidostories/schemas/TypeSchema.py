from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models.reaction import Type


class TypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Type
