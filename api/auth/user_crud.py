from flask import jsonify, request
from flask_jwt_extended import current_user
from sqlalchemy.exc import IntegrityError

from api import db
from api.models import User


from .validators import validate_register_data, validate_update_user


def create():
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


def update():
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


def delete():
    db.session.delete(current_user)
    db.session.commit()

    # TODO: Revoke user token after delete

    response = {'message': 'Done'}
    return jsonify(response), 200
