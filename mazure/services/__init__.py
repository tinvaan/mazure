
from flask import Flask
from collections import namedtuple

from .utils import bp


anchor = __name__
prefix = '/subscriptions'

app = Flask('mazure', instance_relative_config=True)
app.config.from_object('mazure.config')
app.config.from_pyfile('config.py', silent=True)

service = namedtuple('service', ['property', 'blueprint', 'prefix'])
services = dict(
    auth=[
        service('identity', bp(app, 'identity', anchor), None)
    ],
    compute=[
        service('virtual_machines', bp(app, 'virtualmachines', anchor), prefix)
    ],
    storage=[
        service('storage_accounts', bp(app, 'storageaccounts', anchor), prefix)
    ]
)
