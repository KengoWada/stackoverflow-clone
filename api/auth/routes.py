from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, current_user, jwt_required
from sqlalchemy.exc import IntegrityError

from api import db
from api.models import User
from .validators import validate_register_data, validate_update_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    result = validate_register_data(data)
    if not result['is_valid']:
        response = {'message': 'Invalid request', 'error': result['errors']}
        return jsonify(response), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(password=data['password'])

    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError as e:
        error_msg = str(e.orig)
        error_msg = error_msg.split('=')
        error_msg[0] = error_msg[0].split('(')[1][:-1]
        error_msg[1] = error_msg[1].split(')')[0][1:]

        response = {
            'message': f'{error_msg[0].capitalize()}: {error_msg[1]} is already taken.'}
        return jsonify(response), 400

    response = {'message': 'Done', 'user': user.to_dict()}
    return jsonify(response), 201


@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).one_or_none()
    if not user or not user.check_password(data['password']):
        response = {'message': 'Invalid user credentials'}
        return jsonify(response), 400

    response = {
        'message': 'User logged in.',
        'access_token': create_access_token(identity=user),
        'refresh_token': create_refresh_token(identity=user),
    }
    return jsonify(response), 200


class UserAPI(MethodView):
    decorators = [jwt_required()]

    def get(self):
        response = {'message': 'Done', 'user': current_user.to_dict()}
        return jsonify(response), 200

    def put(self):
        data = request.get_json()

        result = validate_update_user(data)
        if not result['is_valid']:
            response = {'message': 'Invalid values',
                        'errors': result['errors']}
            return jsonify(response), 400

        current_user.email = data['email']
        current_user.username = data['username']

        try:
            db.session.commit()
        except IntegrityError as e:
            error_msg = str(e.orig)
            error_msg = error_msg.split('=')
            error_msg[0] = error_msg[0].split('(')[1][:-1]
            error_msg[1] = error_msg[1].split(')')[0][1:]

            response = {
                'message': f'{error_msg[0].capitalize()}: {error_msg[1]} is already taken.'}
            return jsonify(response), 400

        response = {'message': 'Done', 'user': current_user.to_dict()}
        return jsonify(response), 200

    def delete(self):
        db.session.delete(current_user)
        db.session.commit()

        # TODO: Revoke user token after delete

        response = {'message': 'Done'}
        return jsonify(response), 200


auth_bp.add_url_rule(
    '/user',
    view_func=UserAPI.as_view('get_put_delete_user')
)
