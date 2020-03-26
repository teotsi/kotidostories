import enum
from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db
from kotidostories.utils.general_utils import create_id


class Type(str, enum.Enum):
    like = 'like'
    love = 'love'
    laugh = 'laugh'
    inspiring = 'inspiring'


class Reaction(db.Model):
    id = db.Column(db.String(), primary_key=True, default=create_id)
    user_id = db.Column(db.String(), ForeignKey('user.id'), nullable=False, unique=True)
    post_id = db.Column(db.String(), ForeignKey('post.id'), nullable=False)
    type = db.Column(db.Enum(Type), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    from_author = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.type}, {self.date}'
