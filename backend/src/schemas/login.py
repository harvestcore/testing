from marshmallow import fields, Schema


class LoginSchema(Schema):
    token = fields.Str(dump_only=True)
