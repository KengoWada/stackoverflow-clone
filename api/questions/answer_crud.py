from api import db
from api.models import Answer, Question
from flask import jsonify, request
from flask_jwt_extended import current_user


def get_answer_object(question_id, answer_id):
    answer = Answer.query \
        .filter(Answer.id == answer_id, Answer.question_id == question_id) \
        .one_or_none()

    return answer


def create(question_id):
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


def get_all(question_id):
    question = Question.query.get(question_id)
    if not question:
        response = {'message': 'Invalid question ID'}
        return jsonify(response), 400

    answers = [answer.to_dict() for answer in question.answers]

    response = {'message': 'Done', 'answers': answers}
    return jsonify(response), 200


def get_with_id(question_id, answer_id):
    answer = get_answer_object(question_id, answer_id)
    if not answer:
        response = {'message': 'Invalid question/answer ID'}
        return jsonify(response), 400

    response = {'message': 'Done', 'answer': answer.to_dict()}
    return jsonify(response), 200


def like_dislike(question_id, answer_id):
    answer = get_answer_object(question_id, answer_id)
    if not answer:
        response = {'message': 'Invalid question/answer ID'}
        return jsonify(response), 400

    if current_user.has_liked_answer(answer):
        current_user.dislike_answer(answer)
    else:
        current_user.like_answer(answer)

    response = {'message': 'Done'}
    return jsonify(response), 200


def update(question_id, answer_id):
    data = request.get_json()

    answer = get_answer_object(question_id, answer_id)
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


def delete(question_id, answer_id):
    answer = get_answer_object(question_id, answer_id)
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
