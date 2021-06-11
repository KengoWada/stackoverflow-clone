from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required

from api import db
from api.models import Answer, Question

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


@question_bp.route('/')
def get_questions():
    questions = Question.query.all()
    questions = [question.to_dict() for question in questions]

    response = {'message': 'Done', 'questions': questions}
    return jsonify(response), 200


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


@question_bp.route('/<question_id>/answers', methods=['POST'])
@jwt_required()
def answer_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    data = request.get_json()

    answer = Answer(body=data['body'],
                    user_id=current_user.id, question_id=question.id)

    db.session.add(answer)
    db.session.commit()

    response = {'message': 'Done', 'answer': answer.to_dict()}
    return jsonify(response), 201


@question_bp.route('/<question_id>/answers')
def get_question_answers(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    answers = [answer.to_dict() for answer in question.answers]

    response = {'message': 'Done', 'answers': answers}
    return jsonify(response), 200


@question_bp.route('/<question_id>/answers/<answer_id>')
def get_answer_with_id(question_id, answer_id):
    answer = Answer.query \
        .filter(Answer.id == answer_id, Answer.question_id == question_id) \
        .one_or_none()
    if not answer:
        response = {'message': 'Invalid question/answer ID'}
        return jsonify(response), 400

    response = {'message': 'Done', 'answer': answer.to_dict()}
    return jsonify(response), 200


@question_bp.route('/<question_id>/answers/<answer_id>', methods=['PATCH'])
@jwt_required()
def like_answer(question_id, answer_id):
    answer = Answer.query \
        .filter(Answer.id == answer_id, Answer.question_id == question_id) \
        .one_or_none()
    if not answer:
        response = {'message': 'Invalid question/answer ID'}
        return jsonify(response), 400

    if current_user.has_liked_answer(answer):
        current_user.dislike_answer(answer)
    else:
        current_user.like_answer(answer)

    response = {'message': 'Done'}
    return jsonify(response), 200


@question_bp.route('/<question_id>/answers/<answer_id>', methods=['PUT'])
@jwt_required()
def update_answer(question_id, answer_id):
    data = request.get_json()

    answer = Answer.query \
        .filter(Answer.id == answer_id, Answer.question_id == question_id) \
        .one_or_none()
    if not answer:
        response = {'message': 'Invalid question/answer ID'}
        return jsonify(response), 400

    if answer.user_id != current_user.id:
        response = {
            'message': 'You do not have permission to perform this action'}
        return jsonify(response), 403

    answer.body = data['body']
    db.session.commit()

    response = {'message': 'Done', 'answer': answer.to_dict()}
    return jsonify(response), 200


@question_bp.route('/<question_id>/answers/<answer_id>', methods=['DELETE'])
@jwt_required()
def delete_answer(question_id, answer_id):
    answer = Answer.query \
        .filter(Answer.id == answer_id, Answer.question_id == question_id) \
        .one_or_none()
    if not answer:
        response = {'message': 'Invalid question/answer ID'}
        return jsonify(response), 400

    if answer.user_id != current_user.id:
        response = {
            'message': 'You do not have permission to perform this action'}
        return jsonify(response), 403

    db.session.delete(answer)
    db.session.commit()

    response = {'message': 'Done'}
    return jsonify(response), 200
