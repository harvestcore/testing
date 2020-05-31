from marshmallow import fields, Schema


def parse_data(model, data):
    try:
        data = data.decode()
    except (UnicodeDecodeError, AttributeError):
        pass

    if model:
        class AuxSchema(Schema):
            items = fields.List(fields.Nested(model))
            total = fields.Number()
    else:
        class AuxSchema(Schema):
            data = fields.Dict()

    if type(data) is list:
        return AuxSchema().dump({'items': data, 'total': len(data)})
    else:
        return model().dump(data) if model else AuxSchema() \
            .dump({'data': data})
