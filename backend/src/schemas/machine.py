from marshmallow import fields, Schema, validate


class MachineSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    type = fields.Str(required=True, validate=validate.OneOf([
        "local", "remote"
    ]))
    ipv4 = fields.Str()
    ipv6 = fields.Str()
    mac = fields.Str()
    broadcast = fields.Str()
    gateway = fields.Str()
    netmask = fields.Str()
    network = fields.Str()


class MachineSchemaPut(Schema):
    name = fields.Str(required=True)
    data = fields.Nested(MachineSchema, required=True)


class MachineSchemaDelete(Schema):
    name = fields.Str(required=True)
