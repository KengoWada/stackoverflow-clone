from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required

from api import limiter
from . import auth_helpers, user_crud

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@limiter.limit('6 per minute')
def register_user():
    return user_crud.create()


@auth_bp.route('/login', methods=['POST'])
def login_user():
    return auth_helpers.login()


@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit('3 per day')
def forgot_password():
    return auth_helpers.forgot_password()


@auth_bp.route('/reset-password/<token>', methods=['POST'])
@limiter.limit('1 per minute')
def reset_password(token):
    return auth_helpers.reset_password(token=token)


class UserAPI(MethodView):
    decorators = [jwt_required()]

    def get(self):
        response = {'message': 'Done', 'user': current_user.to_dict()}
        return jsonify(response), 200

    def put(self):
        return user_crud.update()

    def delete(self):
        return user_crud.delete()


auth_bp.add_url_rule(
    '/user',
    view_func=UserAPI.as_view('get_put_delete_user')
)
