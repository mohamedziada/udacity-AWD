import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# TODO IMPLEMENT DATABASE URL, done
SQLALCHEMY_DATABASE_URI = 'postgresql://mohamedziada@localhost:5432/fyyur2'
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'postgresql://mohamedziada@localhost:5432/fyyur2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mohamedziada@localhost:5432/fyyur2'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mohamedziada@localhost:5432/fyyur2'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://mohamedziada@localhost:5432/fyyur2'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
