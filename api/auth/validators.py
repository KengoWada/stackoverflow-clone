import re

from cerberus import Validator


class CustomValidator(Validator):
    def _validate_is_email(self, is_email, field, value):
        """
        Test if a value follows the email regex given.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        match = re.match(
            '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$', value)
        if is_email and match == None:
            self._error(field, 'Not a valid email')


def validate_register_data(data):
    schema = {
        'email': {'type': 'string', 'is_email': True, 'required': True},
        'username': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'minlength': 8, 'required': True},
    }

    v = CustomValidator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}


def validate_update_user(data):
    schema = {
        'email': {'type': 'string', 'is_email': True, 'required': True},
        'username': {'type': 'string', 'required': True}
    }

    v = CustomValidator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}
