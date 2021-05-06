
from flask import Flask


app = Flask('mazure', instance_relative_config=True)
app.config.from_object('mazure.config')
app.config.from_pyfile('config.py', silent=True)


with app.app_context():
    from .storageaccounts.views import sa

    app.register_blueprint(sa, url_prefix='/subscriptions')
