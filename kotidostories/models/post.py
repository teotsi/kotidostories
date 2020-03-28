import enum
from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db
from kotidostories.models import user
from kotidostories.utils.general_utils import create_id


class Category(str, enum.Enum):
    horror = 'horror'
    love = 'love'
    funny = 'funny'
    poem = 'poem'
    sci_fi = 'sci-fi'
    whodunit = 'whodunit'
    story = 'story'


class Post(db.Model):
    id = db.Column(db.String(), primary_key=True, default=create_id)
    user_id = db.Column(db.String(), ForeignKey(user.User.id), nullable=False)
    content = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.Enum(Category), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    preview = db.Column(db.String(), nullable=False)
    published = db.Column(db.Boolean(), default=True)
    img = db.Column(db.String(), server_default='pictures/post/default.png')
    comments = db.relationship("Comment", backref="post")
    reactions = db.relationship("Reaction", backref="post")
    user = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.content}, {self.title}, {self.date}'

    def update(self, key, value):
        valid_columns = ['content', 'title', 'date', 'preview','category']
        if key in valid_columns and getattr(self, key) != value:
            return setattr(self, key, value)
