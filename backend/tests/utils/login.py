from src.classes.customer import Customer
from src.classes.login import Login
from src.classes.user import User
from src.classes.mongo_engine import MongoEngine
from tests.utils.auth import Auth
from config.server_environment import TESTING_DATABASE


class TestingLogin:
    engine = None
    headers = None

    def __new__(cls, *args, **kwargs):
        if not cls.engine:
            cls.engine = super(TestingLogin, cls).__new__(cls, *args, **kwargs)

            Customer().set_customer(TESTING_DATABASE)
            MongoEngine().drop(TESTING_DATABASE)
            User().insert({
                'type': 'admin',
                'first_name': 'admin',
                'last_name': 'admin',
                'username': 'admin',
                'email': 'admin@domain.com',
                'password': 'admin'
            })

            logged_user = Login().login(Auth('admin', 'admin'))
            cls.headers = {
                'Content-Type': 'application/json',
                'x-access-token': logged_user.data['token']
            }

        return cls.engine

    def reset(self):
        self.engine = None
        self.headers = None
