from flask import Flask, session, request, current_app, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from config import config
from flask_babel import Babel, lazy_gettext as _l
import logging

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
csrf = CSRFProtect()
babel = Babel()

# for translation
def get_locale():
    # Check if a language is stored in the session
    if 'lang' in session:
        return session['lang']
    # Use the `Accept-Language` header as a fallback
    locale = request.accept_languages.best_match(current_app.config.get('BABEL_SUPPORTED_LOCALES'))
    return locale

def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    
    # for translation
    babel.init_app(app, locale_selector=get_locale)
    app.jinja_env.globals['get_locale'] = get_locale
    
    # logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])    

    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint, url_prefix='/errors')
    
    from app.todos import todos as todos_blueprint
    app.register_blueprint(todos_blueprint, url_prefix='/todos')
    
    from app.products import products as products_blueprint
    app.register_blueprint(products_blueprint, url_prefix='/products')
    
    from app.tickets import tickets as tickets_blueprint
    app.register_blueprint(tickets_blueprint, url_prefix='/tickets')
    
    return app