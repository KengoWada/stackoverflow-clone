from flask import Blueprint, blueprints, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required

from api import db
from api.models import Answer, Question

question_bp = Blueprint('questions', __name__, url_prefix='/questions')


class QuestionCreateList(MethodView):

    @jwt_required()
    def post(self):
        data = request.get_json()

        question = Question(title=data['title'],
                            body=data['body'], user_id=current_user.id)
        db.session.add(question)
        db.session.commit()

        response = {'message': 'Done', 'question': question.to_dict()}
        return jsonify(response), 201

    def get(self):
        questions = Question.query.all()
        questions = [question.to_dict() for question in questions]

        response = {'message': 'Done', 'questions': questions}
        return jsonify(response), 200


class QuestionGetUpdateDelete(MethodView):

    def get(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            response = {'message': 'Invalid question ID'}
            return jsonify(response), 400

        response = {'message': 'Done', 'question': question.to_dict()}
        return jsonify(response), 200

    @jwt_required()
    def put(self, question_id):
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

    @jwt_required()
    def delete(self, question_id):
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


class AnswerCreateList(MethodView):

    @jwt_required()
    def post(self, question_id):
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

    def get(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            response = {'message': 'Invalid question ID'}
            return jsonify(response), 400

        answers = [answer.to_dict() for answer in question.answers]

        response = {'message': 'Done', 'answers': answers}
        return jsonify(response), 200


class AnswerGetUpdateDelete(MethodView):

    def get(self, question_id, answer_id):
        answer = Answer.query \
            .filter(Answer.id == answer_id, Answer.question_id == question_id) \
            .one_or_none()
        if not answer:
            response = {'message': 'Invalid question/answer ID'}
            return jsonify(response), 400

        response = {'message': 'Done', 'answer': answer.to_dict()}
        return jsonify(response), 200

    @jwt_required()
    def patch(self, question_id, answer_id):
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

    @jwt_required()
    def put(self, question_id, answer_id):
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

    @jwt_required()
    def delete(self, question_id, answer_id):
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


@question_bp.route('/mine')
@jwt_required()
def get_my_questions():
    questions = current_user.questions.order_by(Question.created_at.desc())
    questions = [question.to_dict() for question in questions]

    response = {'message': 'Done', 'questions': questions}
    return jsonify(response), 200


question_bp.add_url_rule(
    '/',
    view_func=QuestionCreateList.as_view('post_question_get_questions'),
)

question_bp.add_url_rule(
    '/<question_id>',
    view_func=QuestionGetUpdateDelete.as_view(
        'get_put_delete_question_with_id')
)

question_bp.add_url_rule(
    '/<question_id>/answers',
    view_func=AnswerCreateList.as_view('post_get_answer')
)

question_bp.add_url_rule(
    '/<question_id>/answers/<answer_id>',
    view_func=AnswerGetUpdateDelete.as_view(
        'get_patch_put_delete_answer_with_id')
)
