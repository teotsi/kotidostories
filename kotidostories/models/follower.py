from datetime import datetime

from sqlalchemy import ForeignKey

from kotidostories import db
from kotidostories.models import user


class Follower(db.Model):
    user_id = db.Column(db.String(), ForeignKey(user.User.id), primary_key=True)
    follower_id = db.Column(db.String(), ForeignKey(user.User.id), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
