from flask import Flask, request, abort
from flask_restplus import Api
import tldextract

from config.server_environment import DOCKER_ENABLED
from src.classes.customer import Customer
from src.services.customer import api as customer
from src.services.deploy import api as deploy
from src.services.login import api_login as login
from src.services.login import api_logout as logout
from src.services.machine import api as machine
from src.services.provision import api as provision
from src.services.status import api_status as status
from src.services.status import api_healthcheck as healthcheck
from src.services.user import api as user


app = Flask(__name__)
api = Api(app,
          prefix='/api',
          title='IPManager',
          description='Manage your deploys')
api.add_namespace(customer)
api.add_namespace(healthcheck)
api.add_namespace(login)
api.add_namespace(logout)
api.add_namespace(machine)
api.add_namespace(provision)
api.add_namespace(status)
api.add_namespace(user)

if DOCKER_ENABLED:
    api.add_namespace(deploy)


@app.before_request
def before_request():
    data = tldextract.extract(request.host)
    if Customer().is_customer(data.subdomain):
        Customer().set_customer(data.subdomain)
    else:
        abort(404, "Not found")
