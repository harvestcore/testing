from flask import request
from flask_restplus import Namespace, Resource

from src.classes.docker_engine import DockerEngine
from src.services.login import token_required
from src.schemas.container_operation import *
from src.schemas.image_operation import *
from src.utils.parse_data import parse_data
from src.utils.response_by_success import response_by_success
from src.utils.validate_or_abort import validate_or_abort


api = Namespace(name='deploy', description='Deploy management')


@api.route('/container/single')
class DeployService(Resource):
    @staticmethod
    @token_required
    def post():
        payload = validate_or_abort(BaseSingleContainerProps,
                                    request.get_json())
        container = DockerEngine().get_container_by_id(payload['container_id'])
        if container:
            response = DockerEngine().run_operation_in_object(
                object=container,
                operation=payload['operation'],
                data=payload['data']
            )

            if response is not False:
                return parse_data(None, response)

        return response_by_success(False)


@api.route('/container')
class DeployService(Resource):
    @staticmethod
    @token_required
    def post():
        payload = validate_or_abort(BaseContainersProps, request.get_json())
        data = payload['data']

        if payload['operation'] == 'run':
            data = validate_or_abort(ContainersRunProps, data)
            data['detach'] = True

        if payload['operation'] == 'get':
            data = validate_or_abort(ContainersGetProps, data)

        if payload['operation'] == 'list':
            data = validate_or_abort(ContainersListProps, data)

        if payload['operation'] == 'prune':
            data = validate_or_abort(ContainersPruneProps, data)

        response = DockerEngine().run_container_operation(
            operation=payload['operation'],
            data=data
        )
        schema = ContainerObj if response else None
        return parse_data(schema, response) if response \
            else response_by_success(False)


@api.route('/image/single')
class ImageService(Resource):
    @staticmethod
    @token_required
    def post():
        payload = validate_or_abort(BaseSingleImageProps, request.get_json())
        image = DockerEngine().get_image_by_name(payload['name'])

        if image:
            response = DockerEngine().run_operation_in_object(
                object=image,
                operation=payload['operation'],
                data=payload['data']
            )

            return parse_data(None, response) if response \
                else response_by_success(False)

        return response_by_success(False)


@api.route('/image')
class DeployService(Resource):
    @staticmethod
    @token_required
    def post():
        payload = validate_or_abort(BaseImageProps, request.get_json())
        data = payload['data']

        if payload['operation'] == 'get':
            data = validate_or_abort(ImageGetProps, data)

        if payload['operation'] == 'list':
            data = validate_or_abort(ImageListProps, data)

        if payload['operation'] == 'pull':
            data = validate_or_abort(ImagePullProps, data)

        if payload['operation'] == 'remove':
            data = validate_or_abort(ImageRemoveProps, data)
            data['force'] = True

        if payload['operation'] == 'search':
            data = validate_or_abort(ImageSearchProps, data)

        if payload['operation'] == 'prune':
            data = validate_or_abort(ImagePruneProps, data)

        response = DockerEngine().run_image_operation(
            operation=payload['operation'],
            data=data
        )

        schema = ImageObj if response else None

        if response and payload['operation'] == 'search':
            schema = DockerHubImage

        return parse_data(schema, response) if response \
            else response_by_success(False)
