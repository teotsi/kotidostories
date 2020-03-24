from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models import Reaction


class ReactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Reaction
