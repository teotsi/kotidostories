import enum
from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db


class Type(enum.Enum):
    like = 0
    love = 1
    laugh = 2
    inspiring = 3


class Reaction(db.Model):
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(), ForeignKey('post.id'), nullable=False)
    type = db.Column(db.Enum(Type), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    from_author = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.type}, {self.date}'

    def update(self, key, value):
        valid_columns = ['content']
        if key in valid_columns and getattr(self,key) != value:
            return setattr(self, key, value)