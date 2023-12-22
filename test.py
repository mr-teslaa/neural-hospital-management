from application import *
from application.models import *
import random

def generate_username(first_name, last_name):
    patterns = [
        '{}{}',
        '{}{}{}',
        '{}_{}',
        '{}-{}'
    ]
    username = '{}{}'.format(first_name.lower(), last_name.lower())
    if not User.query.filter_by(username=username).first():
        return username
    username = '{}{}'.format(first_name.capitalize(), last_name)
    if not User.query.filter_by(username=username).first():
        return username
    for i in range(100):
        pattern = random.choice(patterns)
        username = pattern.format(first_name.lower(), last_name.lower(), random.randint(1, 100))
        if not User.query.filter_by(username=username).first():
            return username
    return None


a = input()
b = input()

new = generate_username(a, b)
print('-------------')
print(new)