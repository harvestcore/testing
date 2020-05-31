import os

from src.classes.customer import Customer
from src.classes.user import User

BASE_DATABASE = os.environ.get('BASE_DATABASE', 'ipm_root')

Customer().set_customer(BASE_DATABASE)
User().insert({
    'type': 'admin',
    'first_name': 'Admin',
    'last_name': 'istrator',
    'username': 'admin',
    'email': 'admin@yourdomain.com',
    'password': 'admin'
})
