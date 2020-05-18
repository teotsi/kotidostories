from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from kotidostories.models import Transaction


class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_relationships = True
        model = Transaction
