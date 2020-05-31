from marshmallow import ValidationError, EXCLUDE
from flask_restplus import abort


def validate_or_abort(schema, data):
    try:
        return schema(many=type(data) is list).load(data, unknown=EXCLUDE)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        abort(400, "Bad request")
