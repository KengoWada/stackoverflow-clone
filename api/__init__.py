from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from config import Config


db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from .models import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app=app)
    mail.init_app(app=app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app=app)

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from .questions.routes import question_bp
    app.register_blueprint(question_bp)

    return app


from . import models  # nopep8
