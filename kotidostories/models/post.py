from datetime import datetime
from kotidostories.utils.general_utils import create_id
from sqlalchemy import ForeignKey

from kotidostories import db
from kotidostories.models import user


class Post(db.Model):
    id = db.Column(db.String(), primary_key=True, default=create_id)
    user_id = db.Column(db.String(), ForeignKey(user.User.id), nullable=False)
    content = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    last_edit_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    preview = db.Column(db.String(), nullable=False)
    published = db.Column(db.Boolean(), default=True)
    comments = db.relationship("Comment", backref="post")
    reactions = db.relationship("Reaction", backref="post")

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.content}, {self.title}, {self.date}'

    def update(self, key, value):
        valid_columns = ['content', 'title', 'date','preview']
        if key in valid_columns and getattr(self, key) != value:
            return setattr(self, key, value)
