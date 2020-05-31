from flask import request
from flask_restplus import Resource, Namespace

from src.classes.customer import Customer
from src.classes.user import User
from src.classes.login import Login
from src.schemas.common import QuerySchema
from src.schemas.customer import CustomerSchema, CustomerSchemaDelete, \
    CustomerSchemaPut
from src.services.login import token_required
from src.utils.parse_data import parse_data
from src.utils.response_by_success import response_by_success
from src.utils.validate_or_abort import validate_or_abort


api = Namespace(name='customer', description='Customer management')


@api.route('/query')
class UserServiceGetWithQuery(Resource):
    @staticmethod
    @token_required
    def post():
        user = Login().get_username(request.headers['x-access-token'])

        if user and User().is_admin(user):
            data = validate_or_abort(QuerySchema, request.get_json())
            customer = Customer().find(
                criteria=data['query'],
                projection=data['filter'] if 'filter' in data.keys() else {})

            return parse_data(CustomerSchema, customer.data)
        return response_by_success(False)


@api.route('')
class UserService(Resource):
    @staticmethod
    @token_required
    def post():
        user = Login().get_username(request.headers['x-access-token'])

        if user and User().is_admin(user):
            data = validate_or_abort(CustomerSchema, request.get_json())
            return response_by_success(Customer().insert(data))
        return response_by_success(False)

    @staticmethod
    @token_required
    def put():
        user = Login().get_username(request.headers['x-access-token'])

        if user and User().is_admin(user):
            data = validate_or_abort(CustomerSchemaPut, request.get_json())
            return response_by_success(Customer().update(criteria={
                'domain': data['domain']
            }, data=data['data']))
        return response_by_success(False)

    @staticmethod
    @token_required
    def delete():
        user = Login().get_username(request.headers['x-access-token'])

        if user and User().is_admin(user):
            data = validate_or_abort(CustomerSchemaDelete, request.get_json())
            return response_by_success(Customer().remove(criteria={
                'domain': data['domain']
            }), is_remove=True)
        return response_by_success(False)
