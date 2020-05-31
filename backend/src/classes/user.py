from src.classes.item import Item


class User(Item):
    table_name = 'users'
    table_schema = {
        'type': 1,
        'first_name': 1,
        'last_name': 1,
        'username': 1,
        'email': 1,
        'password': 1,
        'public_id': 1,
        'enabled': 1,
        'deleted': 1
    }

    def __init__(self):
        super(User, self).__init__()

    """
        Inserts a new user.
    """
    def insert(self, data=None):
        if data is not None:
            if data['type'] not in ['admin', 'regular']:
                return False

            current = super(User, self)\
                .find(criteria={'username': data['username'],
                                'email': data['email']})

            if not current.data:
                return super(User, self).insert(data)

        return False

    """
        Checks if the given username belongs to an admin user.
    """
    def is_admin(self, username):
        user = self.find({'username': username})
        if user is not None and user.data is not None:
            return user.data['type'] == 'admin'
