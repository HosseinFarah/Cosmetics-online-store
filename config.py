import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Todo-APP]'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SENDER = 'Todo-APP Admin <' + os.environ.get('MAIL_SENDER') + '>'
    TODO_ADMIN = os.environ.get('TODO_ADMIN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'site.db')
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads/users')
    MAX_CONTRENT_LENGTH = 16 * 1024 * 1024  # 16MB
    MAIL_SENDER= os.environ.get('MAIL_SENDER')
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX= '[Todo-APP]'
    FLASKY_MAIL_SENDER = 'Todo-APP Admin <' + os.environ.get('MAIL_SENDER') + '>'

    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or os.path.join(basedir, 'siteDev.db')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or os.path.join(basedir, 'siteTest.db')
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'site.db')
    
class XAMPPConfig(Config):
    DB_SERVER = os.environ.get('DB_SERVER') or 'localhost'
    DB_USER= os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    DB_NAME = os.environ.get('DB_NAME') or 'flask_todos'
    DB_PORT = os.environ.get('DB_PORT') or '3306'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_SERVER + ':' + DB_PORT + '/' + DB_NAME
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'xampp': XAMPPConfig,
    'default': XAMPPConfig
}
