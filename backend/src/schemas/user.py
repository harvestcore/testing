from marshmallow import fields, Schema, validate

from src.schemas.common import BaseSchema


class UserSchema(BaseSchema):
    type = fields.Str(required=True,
                      validate=validate.OneOf(["admin", "regular"]))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
    public_id = fields.Str(dump_only=True)


class UserSchemaPut(Schema):
    email = fields.Str(required=True)
    data = fields.Nested(UserSchema, required=True)


class UserSchemaDelete(Schema):
    email = fields.Str(required=True)
