from datetime import datetime

from flask_login import UserMixin

from kotidostories import db, login_manager


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String(128), primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    posts = db.relationship("Post", backref="user")
    date = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return f'{self.id}, {self.username}, {self.first_name}, {self.last_name}, {self.email}'
