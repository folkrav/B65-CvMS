from data import data
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = data['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = data['DEV_DB_URL']

class TestingConfig(Config):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = data['TEST_DB_URL']

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = data['PROD_DB_URL']


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
