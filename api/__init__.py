from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from config import Config

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
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
    CORS(app)

    db.init_app(app=app)
    limiter.init_app(app=app)
    mail.init_app(app=app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app=app)

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from .questions.routes import question_bp
    app.register_blueprint(question_bp)

    # Add error handling routes
    @app.errorhandler(404)
    def handle_404(e):
        response = {'message': 'Invalid route'}
        return jsonify(response), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        response = {'message': 'Ratelimit exceeded',
                    'error': str(e.description)}
        return jsonify(response), 429

    @app.errorhandler(500)
    def handle_server_error(e):
        response = {'message': 'An internal error has occured'}
        return jsonify(response), 500

    return app


from . import models  # nopep8
