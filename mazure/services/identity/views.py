
from json import dumps
from flask import Blueprint, jsonify, make_response

from .endpoints import read


auth = Blueprint('identity', __name__)


@auth.route('/common/discovery/instance')
def discover_instance():
    data = read('discover')
    return dumps(data.get('body')), data.get('status'), data.get('headers')
    response = make_response(jsonify(data.get('body')), data.get('status'))
    response.headers = data.get('headers')
    return response


@auth.route('/<subId>/oauth2/v2.0/token', methods=['POST'])
def oauth_token(subId):
    data = read('oauth')
    return dumps(data.get('body')), data.get('status'), data.get('headers')
    response = make_response(jsonify(data.get('body')), data.get('status'))
    response.headers = data.get('headers')
    return response


@auth.route('/<subId>/v2.0/.well-known/openid-configuration')
def openid_config(subId):
    data = read('openid')
    return dumps(data.get('body')), data.get('status'), data.get('headers')
    return (
        data.get('status'),
        data.get('headers'),
        dumps(data.get('body'))
    )
    response = make_response(jsonify(data.get('body')), data.get('status'))
    response.headers = data.get('headers')
    return response
