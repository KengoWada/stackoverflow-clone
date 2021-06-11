from flask import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required


from . import answer_crud, question_crud

question_bp = Blueprint('questions', __name__, url_prefix='/questions')


class QuestionCreateList(MethodView):

    @jwt_required()
    def post(self):
        return question_crud.create()

    def get(self):
        return question_crud.get_all()


class QuestionGetUpdateDelete(MethodView):

    def get(self, question_id):
        return question_crud.get_with_id(question_id=question_id)

    @jwt_required()
    def put(self, question_id):
        return question_crud.update(question_id=question_id)

    @jwt_required()
    def delete(self, question_id):
        return question_crud.delete(question_id=question_id)


@question_bp.route('/mine')
@jwt_required()
def get_my_questions():
    return question_crud.get_mine()


class AnswerCreateList(MethodView):

    @jwt_required()
    def post(self, question_id):
        return answer_crud.create(question_id=question_id)

    def get(self, question_id):
        return answer_crud.get_all(question_id=question_id)


class AnswerGetUpdateDelete(MethodView):

    def get(self, question_id, answer_id):
        return answer_crud.get_with_id(question_id=question_id, answer_id=answer_id)

    @jwt_required()
    def patch(self, question_id, answer_id):
        return answer_crud.like_dislike(question_id=question_id, answer_id=answer_id)

    @jwt_required()
    def put(self, question_id, answer_id):
        return answer_crud.update(question_id=question_id, answer_id=answer_id)

    @jwt_required()
    def delete(self, question_id, answer_id):
        return answer_crud.delete(question_id=question_id, answer_id=answer_id)


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
    view_func=AnswerCreateList.as_view('post_answer_get_answers')
)

question_bp.add_url_rule(
    '/<question_id>/answers/<answer_id>',
    view_func=AnswerGetUpdateDelete.as_view(
        'get_patch_put_delete_answer_with_id')
)
