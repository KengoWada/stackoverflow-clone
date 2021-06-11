from api import db
from api.models import Question
from flask import jsonify, request
from flask_jwt_extended import current_user


def create():
    data = request.get_json()

    question = Question(title=data['title'],
                        body=data['body'], user_id=current_user.id)
    db.session.add(question)
    db.session.commit()

    response = {'message': 'Done', 'question': question.to_dict()}
    return jsonify(response), 201


def get_all():
    questions = Question.query.all()
    questions = [question.to_dict() for question in questions]

    response = {'message': 'Done', 'questions': questions}
    return jsonify(response), 200


def get_with_id(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    response = {'message': 'Done', 'question': question.to_dict()}
    return jsonify(response), 200


def update(question_id):
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


def delete(question_id):
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
