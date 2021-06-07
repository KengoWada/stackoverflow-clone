from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required

from api import db
from api.models import Question

question_bp = Blueprint('questions', __name__, url_prefix='/questions')


@question_bp.route('/', methods=['POST'])
@jwt_required()
def create_question():
    data = request.get_json()

    question = Question(title=data['title'],
                        body=data['body'], user_id=current_user.id)
    db.session.add(question)
    db.session.commit()

    response = {'message': 'Done', 'question': question.to_dict()}
    return jsonify(response), 201


@question_bp.route('/mine')
@jwt_required()
def get_my_questions():
    questions = current_user.questions.order_by(Question.created_at.desc())
    questions = [question.to_dict() for question in questions]

    response = {'message': 'Done', 'questions': questions}
    return jsonify(response), 200


@question_bp.route('/<question_id>')
def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    response = {'message': 'Done', 'question': question.to_dict()}
    return jsonify(response), 200


@question_bp.route('/<question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    if question.user_id != current_user.id:
        response = {'message': 'Invalid request'}
        return jsonify(response), 403

    data = request.get_json()
    question.update(data)
    db.session.commit()

    response = {'message': 'Done', 'question': question.to_dict()}
    return jsonify(response), 200


@question_bp.route('/<question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    if question.user_id != current_user.id:
        response = {'message': 'Invalid request'}
        return jsonify(response), 403

    db.session.delete(question)
    db.session.commit()

    response = {'message': 'Done'}
    return jsonify(response), 200


@question_bp.route('/')
def get_questions():
    questions = Question.query.all()
    questions = [question.to_dict() for question in questions]

    response = {'message': 'Done', 'questions': questions}
    return jsonify(response), 200
