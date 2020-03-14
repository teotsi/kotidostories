from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db


class Comment(db.Model):
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(), ForeignKey('post.id'), nullable=False)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    from_author = db.Column(db.Boolean(), default=False)
    hidden = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.content}, {self.date}'

    def update(self, key, value):
        valid_columns = ['content']
        if key in valid_columns and getattr(self,key) != value:
            return setattr(self, key, value)