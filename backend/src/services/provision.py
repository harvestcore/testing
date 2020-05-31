from flask import request
from flask_restplus import Namespace, Resource

from src.classes.ansible.ansible_engine import AnsibleEngine
from src.classes.ansible.host import Host
from src.classes.ansible.playbook import Playbook
from src.schemas.common import QuerySchema
from src.schemas.provision import BaseHost, BasePlaybook, \
    ProvisionSchemaDelete, ProvisionSchemaPut, ProvisionRunResponseSchema,\
    ProvisionRunSchema, ProvisionPlaybookPut
from src.services.login import token_required
from src.utils.response_by_success import response_by_success
from src.utils.validate_or_abort import validate_or_abort
from src.utils.parse_data import parse_data


api = Namespace(name='provision', description='Provision management')


####################################################################
# HOSTS
####################################################################

@api.route('/hosts/<string:name>')
class HostServiceGet(Resource):
    @staticmethod
    @token_required
    def get(name):
        user = Host().find(criteria={'name': name})
        return parse_data(BaseHost, user.data)


@api.route('/hosts/query')
class HostService(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(QuerySchema, request.get_json())
        host = Host().find(criteria=data['query'],
                           projection=data['filter'] if 'filter' in data.keys()
                           else {})
        return parse_data(BaseHost, host.data)


@api.route('/hosts')
class HostsService(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(BaseHost, request.get_json())
        return response_by_success(Host().insert(data))

    @staticmethod
    @token_required
    def put():
        data = validate_or_abort(ProvisionSchemaPut, request.get_json())
        return response_by_success(Host().update(criteria={
            'name': data['name']
        }, data=data['data']))

    @staticmethod
    @token_required
    def delete():
        data = validate_or_abort(ProvisionSchemaDelete, request.get_json())
        return response_by_success(Host().remove(criteria={
            'name': data['name']
        }), is_remove=True)


####################################################################
# PLAYBOOKS
####################################################################

@api.route('/playbook/<string:name>')
class PlaybookServiceGet(Resource):
    @staticmethod
    @token_required
    def get(name):
        user = Playbook().find(criteria={'name': name})
        return parse_data(BasePlaybook, user.data)


@api.route('/playbook/query')
class PlaybookService(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(QuerySchema, request.get_json())
        playbook = Playbook().find(
            criteria=data['query'],
            projection=data['filter'] if 'filter' in data.keys() else {}
        )
        return parse_data(BasePlaybook, playbook.data)


@api.route('/playbook')
class PlaybookService(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(BasePlaybook, request.get_json())
        return response_by_success(Playbook().insert(data))

    @staticmethod
    @token_required
    def put():
        data = validate_or_abort(ProvisionPlaybookPut, request.get_json())
        return response_by_success(Playbook().update(criteria={
            'name': data['name']
        }, data=data['data']))

    @staticmethod
    @token_required
    def delete():
        data = validate_or_abort(ProvisionSchemaDelete, request.get_json())
        return response_by_success(Playbook().remove(criteria={
            'name': data['name']
        }), is_remove=True)


####################################################################
# PROVISION
####################################################################

@api.route('')
class ProvisionService(Resource):
    @staticmethod
    @token_required
    def post():
        data = validate_or_abort(ProvisionRunSchema, request.get_json())
        results = AnsibleEngine().run_playbook(
            hosts=data['hosts'],
            playbook=data['playbook'],
            passwords=data['passwords']
        )

        if results:
            return parse_data(
                ProvisionRunResponseSchema, {
                    'result': results
                }
            )

        return response_by_success(False)
