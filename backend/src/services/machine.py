from flask import request
from flask_restplus import Resource, Namespace

from src.classes.machine import Machine
from src.utils.validate_or_abort import validate_or_abort
from src.schemas.common import QuerySchema
from src.schemas.machine import MachineSchema, MachineSchemaDelete,\
    MachineSchemaPut
from src.services.login import token_required
from src.utils.parse_data import parse_data
from src.utils.response_by_success import response_by_success


api = Namespace(name='machine', description='Machines management')


@api.route('/<string:name>')
class MachineServiceGet(Resource):
    @staticmethod
    @token_required
    def get(name):
        user = Machine().find(criteria={'name': name})
        return parse_data(MachineSchema, user.data)


@api.route('/query')
class MachineServiceGetWithQuery(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(QuerySchema, request.get_json())
        user = Machine().find(
            criteria=data['query'],
            projection=data['filter'] if 'filter' in data.keys() else {}
        )

        return parse_data(MachineSchema, user.data)


@api.route('')
class MachineService(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(MachineSchema, request.get_json())
        return response_by_success(Machine().insert(data))

    @staticmethod
    @token_required
    def put():
        data = validate_or_abort(MachineSchemaPut, request.get_json())
        return response_by_success(Machine().update(criteria={
            'name': data['name']
        }, data=data['data']))

    @staticmethod
    @token_required
    def delete():
        data = validate_or_abort(MachineSchemaDelete, request.get_json())
        return response_by_success(Machine().remove(criteria={
            'name': data['name']
        }), is_remove=True)
