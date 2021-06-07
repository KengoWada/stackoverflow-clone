from flask import Flask


def create_app():
    app = Flask(__name__)

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from .questions.routes import question_bp
    app.register_blueprint(question_bp)

    return app
