import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = os.environ.get('DEBUG', default=True)
    TESTING = os.environ.get('TESTING')
    SECRET_KEY = os.environ.get('SECRET_KEY', default='So safe')
    ENV = os.environ.get('ENV', default='development')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///.developmentdb.sqlite?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_FOR_FLASK')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USE_SSL = False
    # SESSION_COOKIE_SECURE = True,
    SESSION_COOKIE_HTTPONLY = True,
    SESSION_COOKIE_SAMESITE = 'Strict'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestConfig(Config):
    ENV = os.environ.get('ENV', default='development')
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
