from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db
from kotidostories.models import user
from kotidostories.utils.general_utils import create_id


class Transaction(db.Model):
    id = db.Column(db.String(), primary_key=True, default=create_id)
    date = db.Column(db.DateTime, default=datetime.now)
    to_user = db.Column(db.String(), ForeignKey(user.User.id), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    company_amount = db.Column(db.Float(), nullable=False)

    def __init__(self, **kwargs):
        kwargs['company_amount'] = float(kwargs['amount']) * 0.2
        super(Transaction, self).__init__(**kwargs)

    def __repr__(self):
        return f'{self.id}, {self.to_user}, {self.amount}, {self.company_amount}, {self.date}'
