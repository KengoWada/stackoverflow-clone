from cerberus import Validator


def validate_question(data):
    schema = {
        'title': {'type': 'string', 'maxlength': 100, 'required': True},
        'body': {'type': 'string', 'maxlength': 256, 'required': True},
    }

    v = Validator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}


def validate_answer(data):
    schema = {
        'body': {'type': 'string', 'required': True},
    }

    v = Validator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}
