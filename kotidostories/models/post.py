from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db
from kotidostories.models import user


class Post(db.Model):
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), ForeignKey(user.User.id), nullable=False)
    content = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'content': self.content,
                'title': self.title,
                'date': self.date}

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.content}, {self.title}, {self.date}'
