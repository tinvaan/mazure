
from flask import jsonify, make_response, Blueprint

from .models import read


auth = Blueprint('identity', __name__)


@auth.route('/common/discovery/instance')
def discover_instance():
    data = read('discover')
    response = make_response(jsonify(data.get('body')), data.get('status'))
    response.headers = data.get('headers')
    return response


@auth.route('/<subId>/oauth2/v2.0/token', methods=['POST'])
def oauth_token(subId):
    data = read('oauth')
    response = make_response(jsonify(data.get('body')), data.get('status'))
    response.headers = data.get('headers')
    return response


@auth.route('/<subId>/v2.0/.well-known/openid-configuration')
def openid_config(subId):
    data = read('openid')
    response = make_response(jsonify(data.get('body')), data.get('status'))
    response.headers = data.get('headers')
    return response
