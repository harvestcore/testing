from marshmallow import fields, Schema

from src.schemas.common import BaseSchema


class BaseHost(BaseSchema):
    name = fields.Str(required=True)
    ips = fields.List(fields.Str(), required=True)


class BasePlaybook(BaseSchema):
    name = fields.Str(required=True)
    playbook = fields.Dict(required=True)


class ProvisionSchemaPut(Schema):
    name = fields.Str(required=True)
    data = fields.Nested(BaseHost, required=True)


class ProvisionPlaybookPut(Schema):
    name = fields.Str(required=True)
    data = fields.Dict(required=True)


class ProvisionSchemaDelete(Schema):
    name = fields.Str(required=True)


class ProvisionPasswords(Schema):
    conn_pass = fields.Str()
    become_pass = fields.Str()


class ProvisionRunSchema(Schema):
    hosts = fields.List(fields.Str(), required=True)
    playbook = fields.Str(required=True)
    passwords = fields.Nested(ProvisionPasswords(), required=True)


class ProvisionRunResponseSchema(Schema):
    result = fields.Str()
