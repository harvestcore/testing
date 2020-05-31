from marshmallow import fields, Schema, validate


class ImageObj(Schema):
    id = fields.Str()
    labels = fields.Dict()
    short_id = fields.Str()
    tags = fields.List(fields.Str)


class RegistryDataObj(Schema):
    id = fields.Str()
    short_id = fields.Str()


class BaseSingleImageProps(Schema):
    name = fields.Str(required=True)
    operation = fields.Str(required=True, validate=validate.OneOf([
        "history", "reload"
    ]))
    data = fields.Dict(required=True)


class SingleImageTagProps(Schema):
    repository = fields.Str(required=True)
    tag = fields.Str(required=True)
    force = fields.Bool()


class BaseImageProps(Schema):
    operation = fields.Str(required=True, validate=validate.OneOf([
        "list", "get", "prune", "pull", "remove", "search"
    ]))
    data = fields.Dict(required=True)


class ImageGetProps(Schema):
    name = fields.Str(required=True)


class ImageFilterProps(Schema):
    dangling = fields.Bool()
    label = fields.List(fields.Str)


class ImageListProps(Schema):
    name = fields.Str()
    all = fields.Bool(default=True)
    filters = fields.Nested(ImageFilterProps)


class ImagePullProps(Schema):
    repository = fields.Str()
    tag = fields.Str()
    auth_config = fields.Dict()
    platform = fields.Str()


class ImagePruneProps(Schema):
    filters = fields.Nested(ImageFilterProps)


class ImageRemoveProps(Schema):
    image = fields.Str(required=True)
    force = fields.Bool(default=True)
    noprune = fields.Bool()


class ImageSearchProps(Schema):
    term = fields.Str(required=True)


class DockerHubImage(Schema):
    star_count = fields.Int()
    is_official = fields.Bool()
    name = fields.Str()
    is_automated = fields.Bool()
    description = fields.Str()
