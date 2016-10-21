from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import configs
from .main import main as main_blueprint


bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    """Factory method to create a CvMS app instance."""
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    app.register_blueprint(main_blueprint)

    return app
