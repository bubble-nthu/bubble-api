import os
import yaml
from yaml.loader import SafeLoader
import os.path

# Open the file and load the file
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SECURITY_PASSWORD_SALT  = 'my_precious_two'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUBBLE_POSTS_PER_PAGE = 10
    BUBBLE_FOLLOWERS_PER_PAGE = 10
    BUBBLE_COMMENTS_PER_PAGE = 10
    SSL_REDIRECT = False
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_API_KEY = os.environ.get('MAIL_API_KEY')
    MAIL_API_URL = os.environ.get('MAIL_API_URL')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    with open('secrets.yml') as f:
        secrets = yaml.load(f, Loader=SafeLoader)
        secrets = secrets['development']
    DEBUG = True
    MSG_KEY = secrets['MSG_KEY']
    BUBBLE_API_URL = "http://127.0.0.1:5000"
    MAIL_API_KEY = secrets['SENDGRID_API_KEY']
    MAIL_API_URL = secrets['SENDGRID_API_URL']
    AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
    #MAIL_SENDER = secrets['SENDGRID_MAIL_SENDER']
    #MAIL_DEFAULT_SENDER = secrets['SENDGRID_MAIL_SENDER']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    with open('secrets.yml') as f:
        secrets = yaml.load(f, Loader=SafeLoader)
        secrets = secrets['test']
    TESTING = True
    MSG_KEY = secrets['MSG_KEY']
    BUBBLE_API_URL = "http://127.0.0.1:5000"
    MAIL_API_KEY = secrets['SENDGRID_API_KEY']
    MAIL_API_URL = secrets['SENDGRID_API_URL']
    AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
    #MAIL_SENDER = secrets['SENDGRID_MAIL_SENDER']
    #MAIL_DEFAULT_SENDER = secrets['SENDGRID_MAIL_SENDER']
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    MSG_KEY = os.environ.get('MSG_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class HerokuConfig(ProductionConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    # rest of connection code using the connection string `uri`

    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        try:
            from werkzeug.middleware.proxy_fix import ProxyFix
        except ImportError:
            from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'docker': DockerConfig,

    'default': DevelopmentConfig,
}