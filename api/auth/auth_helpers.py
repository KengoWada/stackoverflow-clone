from flask import jsonify, request, url_for
from flask_jwt_extended import create_access_token

from api import db
from api.models import User
from api.utils import send_mail, get_token, verify_token

from .validators import validate_forgot_password, validate_reset_password


def login():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).one_or_none()
    if not user or not user.check_password(data['password']):
        response = {'message': 'Invalid user credentials'}
        return jsonify(response), 400

    response = {
        'message': 'User logged in.',
        'access_token': create_access_token(identity=user),
    }
    return jsonify(response), 200


def forgot_password():
    data = request.get_json()

    result = validate_forgot_password(data)
    if not result['is_valid']:
        response = {'message': 'Invalid email'}
        return jsonify(response), 400

    response = {'message': 'Done'}

    user = User.query.filter(User.email == data['email']).one_or_none()
    if not user:
        return jsonify(response), 200

    token = get_token(user.email)
    path = url_for('.reset_password', token=token)[1:]
    url = f'{request.host_url}{path}'

    user.password_reset_token = token
    db.session.commit()

    subject = 'Reset Account Password'
    body = f'''.base_url
    Hey {user.username},
    You have requested to change your password. Click on the link:
    {url}
    If this is not you, don't click the link.

    Thanks,
    MGT
    '''
    recipient = user.email

    send_mail(subject=subject, body=body, recipient=recipient)

    return jsonify(response), 200


def reset_password(token):
    data = request.get_json()

    result = validate_reset_password(data)
    if not result['is_valid']:
        response = {'message': 'Invalid password'}
        return jsonify(response), 400

    email = verify_token(token)
    if not email:
        response = {'message': 'Invalid token'}
        return jsonify(response), 400

    user = User.query.filter(User.email == email).one_or_none()
    if not user or user.password_reset_token != token:
        response = {'message': 'Invalid token'}
        return jsonify(response), 400

    user.set_password(data['password'])
    user.password_reset_token = ''
    db.session.commit()

    response = {'message': 'Done. You can now log in'}
    return jsonify(response), 200
