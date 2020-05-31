from marshmallow import fields, Schema, validate

from src.schemas.image_operation import ImageObj


class BaseSingleContainerProps(Schema):
    container_id = fields.Str(required=True)
    operation = fields.Str(required=True, validate=validate.OneOf([
        "kill", "logs", "pause", "reload", "rename", "restart",
        "stop", "unpause"
    ]))
    data = fields.Dict(required=True)


class BaseContainersProps(Schema):
    operation = fields.Str(required=True, validate=validate.OneOf([
        "run", "get", "list", "prune"
    ]))
    data = fields.Dict(required=True)


class ContainerObj(Schema):
    id = fields.Str()
    labels = fields.Dict()
    name = fields.Str()
    short_id = fields.Str()
    status = fields.Str()
    image = fields.Nested(ImageObj)


class ContainersRunProps(Schema):
    image = fields.Str(required=True)
    command = fields.List(fields.Str())
    auto_remove = fields.Bool()
    detach = fields.Bool(default=True)
    entrypoint = fields.List(fields.Str())
    environment = fields.Dict()
    hostname = fields.Str()
    mounts = fields.List(fields.Str())
    name = fields.Str()
    network = fields.Str()
    ports = fields.Dict()
    user = fields.Str()
    volumes = fields.Dict()
    working_dir = fields.Str()
    remove = fields.Bool()


class ContainersGetProps(Schema):
    container_id = fields.Str(required=True)


class ContainersFilterProps(Schema):
    exited = fields.Bool()
    status = fields.Str(validate=validate.OneOf([
        "restarting", "running", "paused", "exited"
    ]))
    id = fields.Str()
    name = fields.Str()


class ContainersListProps(Schema):
    all = fields.Bool()
    since = fields.Str()
    before = fields.Str()
    filters = fields.Nested(ContainersFilterProps)


class ContainersPruneProps(Schema):
    filters = fields.Nested(ContainersFilterProps)
