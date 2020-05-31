from marshmallow import fields, Schema

from src.schemas.common import BaseSchema


class CustomerSchema(BaseSchema):
    domain = fields.Str(required=True)
    db_name = fields.Str(required=True)
    enabled = fields.Str(dump_only=True)
    deleted = fields.Str(dump_only=True)


class CustomerBaseSchemaPut(BaseSchema):
    domain = fields.Str(required=True)
    db_name = fields.Str(required=True)
    enabled = fields.Boolean()


class CustomerSchemaPut(Schema):
    domain = fields.Str(required=True)
    data = fields.Nested(CustomerBaseSchemaPut, required=True)


class CustomerSchemaDelete(Schema):
    domain = fields.Str(required=True)
