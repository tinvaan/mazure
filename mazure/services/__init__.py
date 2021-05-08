
from json import dumps
from flask import Flask, request


app = Flask('mazure', instance_relative_config=True)
app.config.from_object('mazure.config')
app.config.from_pyfile('config.py', silent=True)


@app.after_request
def logit(response):
    try:
        body = request.get_json()
    except Exception:
        body = request.get_data()

    app.logger.info(dumps({
        'ip': request.remote_addr,
        'host': request.host.split(':', 1).pop(0),
        'args': dict(request.args),
        'body': body
    }, indent=2))

    return response


with app.app_context():
    from .storageaccounts.views import sa

    app.register_blueprint(sa, url_prefix='/subscriptions')
