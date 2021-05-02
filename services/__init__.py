
from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('services.config')
app.config.from_pyfile('config.py', silent=True)


with app.app_context():
    from services.storageaccounts.views import sa

    app.register_blueprint(sa, url_prefix='/subscriptions')
