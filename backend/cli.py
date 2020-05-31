from PyInquirer import prompt

from src.classes.customer import Customer
from src.classes.user import User


def error():
    print("Something went wrong, please try again.")


def create_customer(c):
    return Customer().insert(c)


def list_customers(enabled=None):
    if enabled is None:
        data = Customer().find({}, projection={'domain': 1}).data
    else:
        data = Customer().find({'enabled': enabled},
                               projection={'domain': 1}).data
    if type(data) is dict:
        return [{'name': data['domain']}]
    if data is not None:
        return [{'name': item['domain']} for item in data]

    return []


def enable_customer(enabled, name):
    return Customer().update({'domain': name}, data={'enabled': enabled})


def create_user(u, c):
    if Customer().is_customer(c) is not None:
        Customer().set_customer(c)
        return User().insert(u)

    return False


operations = [
    {
        'type': 'list',
        'name': 'operation',
        'message': 'What you want to do?',
        'choices': [
            {
                'name': 'Create a customer'
            },
            {
                'name': 'Enable a customer'
            },
            {
                'name': 'Disable a customer'
            },
            {
                'name': 'Add user to customer'
            },
            {
                'name': 'Exit'
            }
        ]
    }
]

if __name__ == '__main__':
    answer = prompt(operations)['operation']

    if answer == 'Create a customer':
        customer = prompt([
            {
                'type': 'input',
                'name': 'domain',
                'message': 'Enter a customer name',
                'validate': lambda value: value != ''
            },
            {
                'type': 'input',
                'name': 'db_name',
                'message': 'Enter a database name',
                'validate': lambda value: value != ''
            }
        ])

        if create_customer(customer):
            print("Customer created successfully")
        else:
            error()

    elif answer == 'Enable a customer':
        data = list_customers(enabled=False)
        if len(data) == 0:
            print("There are no customers disabled")
            exit(1)

        customer = prompt({
            'type': 'list',
            'name': 'customer',
            'message': 'Which customer do you want to enable?',
            'choices': data
        })

        if enable_customer(True, customer['customer']):
            print("User enabled successfully")
        else:
            error()

    elif answer == 'Disable a customer':
        data = list_customers(enabled=True)
        if len(data) == 0:
            print("There are no customers enabled")
            exit(1)

        customer = prompt({
            'type': 'list',
            'name': 'customer',
            'message': 'Which customer do you want to disable?',
            'choices': data
        })

        if enable_customer(False, customer['customer']):
            print("User disabled successfully")
        else:
            error()

    elif answer == 'Add user to customer':
        data = list_customers()
        if len(data) == 0:
            print("There are no customers enabled")
            exit(1)

        customer = prompt({
            'type': 'list',
            'name': 'customer',
            'message': 'In which customer do you want to add a user?',
            'choices': data
        })

        user = prompt([
            {
                'type': 'input',
                'name': 'first_name',
                'message': 'Enter the first name',
                'validate': lambda value: value != ''
            },
            {
                'type': 'input',
                'name': 'last_name',
                'message': 'Enter the last name',
                'validate': lambda value: value != ''
            },
            {
                'type': 'input',
                'name': 'username',
                'message': 'Enter a username',
                'validate': lambda value: value != ''
            },
            {
                'type': 'input',
                'name': 'email',
                'message': 'Enter an email',
                'validate': lambda value: value != ''
            },
            {
                'type': 'input',
                'name': 'password',
                'message': 'Enter a password',
                'validate': lambda value: value != ''
            },
            {
                'type': 'input',
                'name': 'type',
                'message': 'Enter a type of user [admin, regular]',
                'validate': lambda value: value in ['admin', 'regular']
            }
        ])

        if create_user(user, customer['customer']):
            print("User created successfully")
        else:
            error()

    elif answer == 'Exit':
        exit(0)
