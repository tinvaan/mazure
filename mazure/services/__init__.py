
from flask import Flask
from collections import namedtuple

from .utils import blueprint


service = namedtuple('service', ['prefix', 'property', 'blueprint'])

app = Flask('mazure', instance_relative_config=True)
app.config.from_object('mazure.config')
app.config.from_pyfile('config.py', silent=True)

app.config['services'] = dict(
    auth=[
        service(
            None,
            'identity',
            blueprint(app, 'identity')
        )
    ],
    compute=[
        service(
            '/subscriptions',
            'virtual_machine',
            blueprint(app, 'virtualmachines')
        )
    ],
    resources=[
        service(
            '/subscriptions',
            'resource_groups',
            blueprint(app, 'resourcegroups')
        )
    ],
    storage=[
        service(
            '/subscriptions',
            'storage_accounts',
            blueprint(app, 'storageaccounts')
        )
    ]
)
