
from flask import Flask


app = Flask('mazure', instance_relative_config=True)
app.config.from_object('mazure.config')
app.config.from_pyfile('config.py', silent=True)

with app.app_context():
    from .identity.views import auth
    from .storageaccounts.views import sa
    from .virtualmachines.views import vm

    app.register_blueprint(auth)
    app.register_blueprint(sa, url_prefix='/subscriptions')
    app.register_blueprint(vm, url_prefix='/subscriptions')
