from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from kotidostories import db, login_manager, secret


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
    id = db.Column(db.String(128), primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")

    def get_reset_token(self, expires=1800):
        s = Serializer(secret, expires)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def __repr__(self):
        return f'{self.id}, {self.username}, {self.first_name}, {self.last_name}, {self.email}, {self.posts}'
