import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = os.environ.get('DEBUG')
    TESTING = os.environ.get('TESTING')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENV = os.environ.get('ENV', default='development')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///.developmentdb.sqlite?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
