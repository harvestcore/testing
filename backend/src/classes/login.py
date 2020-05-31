import datetime as dt
from cryptography.fernet import Fernet
import jwt

from config.server_environment import ENC_KEY, JWT_ENC_KEY
from src.classes.item import Item
from src.classes.user import User


class Login(Item):
    table_name = 'login'
    table_schema = {
        'token': 1,
        'username': 1,
        'exp': 1,
        'login_time': 1,
        'public_id': 1
    }

    def __init__(self):
        super(Login, self).__init__()

        # Clean previous users
        current_logged_in = self.find()
        if current_logged_in.data is not None:
            if type(current_logged_in.data) is dict:
                date_now = current_logged_in.data['exp']
                if date_now < dt.datetime.utcnow().timestamp():
                    self.remove({
                        'username': current_logged_in.data['username']
                    })
            elif type(current_logged_in.data) is list:
                for user in current_logged_in.data:
                    date_now = user['exp']
                    if int(date_now) < round(dt.datetime.utcnow().timestamp()):
                        self.remove(
                            {'username': user['username']})

    """
        Performs the login of the user.
    """
    def login(self, auth):
        user = User().find({'username': auth.username})

        if not user.data:
            return False

        f = Fernet(ENC_KEY)
        if f.decrypt(user.data['password'].encode()).decode() == auth.password:
            login_time = round(dt.datetime.utcnow().timestamp())
            exp = dt.datetime.utcnow() + dt.timedelta(hours=12)
            exp = round(exp.timestamp())
            token = jwt.encode({
                'public_id': user.data['public_id'],
                'exp': exp
            }, JWT_ENC_KEY)

            existing = self.find({'username': auth.username})
            if existing.data is None:
                self.insert(data={
                    'public_id': user.data['public_id'],
                    'token': token.decode('UTF-8'),
                    'username': auth.username,
                    'exp': exp,
                    'login_time': login_time
                })
            else:
                self.update(criteria={'username': auth.username}, data={
                    'public_id': user.data['public_id'],
                    'token': token.decode('UTF-8'),
                    'username': auth.username,
                    'exp': exp,
                    'login_time': login_time
                })

            return self.find({'public_id': user.data['public_id']})
        return False

    """
        Performs the logout of the user.
    """
    def logout(self, username):
        user = User().find({'username': username})

        if not user.data:
            return False

        return self.remove({'username': username}, force=True)

    """
        Decodes the given token and returns the 'session' stored.
    """
    def token_access(self, token):
        data = jwt.decode(token, JWT_ENC_KEY, algorithms=['HS256'])
        return self.find({'public_id': data['public_id']})

    """
        Returns the username that it is stored in the given token.
    """
    def get_username(self, token):
        user = self.token_access(token)
        if user and user.data:
            return user.data['username']
        return None
