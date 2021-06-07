from flask import Blueprint

question_bp = Blueprint('questions', __name__, url_prefix='/questions')


@question_bp.route('/')
def index():
    return 'Hello from questions'
