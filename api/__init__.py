from config import Config
from flask import Flask
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from .questions.routes import question_bp
    app.register_blueprint(question_bp)

    return app

from . import models
