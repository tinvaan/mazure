
from json import loads
from mongoengine.errors import ValidationError
from flask import Blueprint, request, jsonify, make_response

from .models import DatabaseAccount


dba = Blueprint('dbaccount', __name__)


@dba.route('/')
def list_databases():
    """
    Lists the databases under a database account.

    Ref: https://docs.microsoft.com/en-us/rest/api/cosmos-db/list-databases
    """
    dbs = DatabaseAccount.objects.all()
    return jsonify({
        '_rid': '',
        'Databases': dbs.to_json(),
        '_count': dbs.count()
    })


@dba.route('/', methods=['POST'])
def create_database():
    """
    Creates a new database in the database account.

    Ref: https://docs.microsoft.com/en-us/rest/api/cosmos-db/create-a-database
    """
    try:
        db = DatabaseAccount(**request.get_json(force=True))
        db.save()
        return jsonify(loads(db.to_json()))
    except ValidationError:
        return make_response(jsonify({
            'error': {
                'code': 'InvalidParameters',
                'message': 'Incorrect parameter values provided for create'
            }
        }), 400)


@dba.route('/<dbId>')
def get_database(dbId):
    """
    Retrieves a database under a database account.

    Ref: https://docs.microsoft.com/en-us/rest/api/cosmos-db/get-a-database
    """
    try:
        return jsonify(loads(DatabaseAccount.objects.get(rid=dbId).to_json()))
    except DatabaseAccount.DoesNotExist:
        return make_response(jsonify({
            'error': {
                'code': 'ResourceNotFound',
                'message': 'Requested database account was not found'
            }
        }), 404)


@dba.route('/<dbId>', methods=['DELETE'])
def delete_database(dbId):
    """
    Deletes an existing database in the database account.

    Ref: https://docs.microsoft.com/en-us/rest/api/cosmos-db/delete-a-database
    """
    try:
        DatabaseAccount.objects.get(rid=dbId).delete()
    except DatabaseAccount.DoesNotExist:
        return ('', 404)
    return ('', 204)
