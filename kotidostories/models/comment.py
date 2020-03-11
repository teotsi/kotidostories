from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db


class Comment(db.Model):
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(), ForeignKey('post.id'), nullable=False)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'content': self.content,
                'date': self.date}

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.content}, {self.date}'
