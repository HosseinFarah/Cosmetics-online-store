from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from config import config
from flask_mail import Mail
import logging

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
csrf = CSRFProtect()
mail = Mail()


def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('app.log'),logging.StreamHandler()])
    

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    
    from app.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)
    
    from app.todos import todos as todos_blueprint
    app.register_blueprint(todos_blueprint, url_prefix='/todos')
    

    return app