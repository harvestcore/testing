from marshmallow import fields, Schema


class BaseSchema(Schema):
    enabled = fields.Bool(dump_only=True)
    deleted = fields.Bool(dump_only=True)


class QuerySchema(Schema):
    query = fields.Dict(required=True)
    filter = fields.Dict()
