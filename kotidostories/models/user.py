from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from kotidostories import db, login_manager, secret
from kotidostories.utils.general_utils import create_id


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


def verify_reset_token(token):
    s = Serializer(secret)
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String(128), primary_key=True, default=create_id)
    username = db.Column(db.String(), unique=True, nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now)
    posts = db.relationship("Post", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    reactions = db.relationship("Reaction", backref="user")
    followers = db.relationship("User",
                                secondary="follower",
                                primaryjoin="User.id==follower.c.user_id",
                                secondaryjoin="User.id==follower.c.follower_id",
                                backref="follower")
    following = db.relationship("User",
                                secondary="follower",
                                primaryjoin="User.id==follower.c.follower_id",
                                secondaryjoin="User.id==follower.c.user_id",
                                backref="followee")

    def get_reset_token(self, expires=1800):
        s = Serializer(secret, expires)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def __repr__(self):
        return f'{self.id}, {self.username}, {self.first_name}, {self.last_name}, {self.email}, {self.posts}'
