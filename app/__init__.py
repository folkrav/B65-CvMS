from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_misaka import Misaka
from config import configs


bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()
misaka = Misaka()
login = LoginManager()
login.session_protection = 'strong'
login.login_view = 'auth.login'

def create_app(config_name):
    """Factory method to create a CvMS app instance."""
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    # Start extensions
    login.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    misaka.init_app(app)

    # Register blueprints to the app
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authentication')
    from app.users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app
