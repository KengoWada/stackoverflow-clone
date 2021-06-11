import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = bool(os.environ.get('DEBUG')) or False
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Flask SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Settings
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # Flask-Mail Settings
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
