
from .models import ResourceGroup

from json import loads
from flask import Blueprint, request, jsonify, make_response
from mongoengine.errors import ValidationError, FieldDoesNotExist


rg = Blueprint('resourcegroups', __name__)


@rg.route('/<subId>/resourcegroups')
def list_resource_groups(subId):
    """
    Gets all the resource groups for a subscription.

    Ref: https://docs.microsoft.com/en-us/rest/api/resources/resource-groups/list
    """
    groups = ResourceGroup.objects.all()
    return jsonify({'value': loads(groups.to_json())})


@rg.route('/<subId>/resourcegroups/<rgname>')
def get_resource_group(subId, rgname):
    """
    Gets a resource group.

    Ref: https://docs.microsoft.com/en-us/rest/api/resources/resource-groups/get
    """
    try:
        group = ResourceGroup.objects.get(subscription=subId, name=rgname)
        return jsonify(loads(group.to_json()))
    except ResourceGroup.DoesNotExist:
        return make_response({
            'error': {
                'code': 'ResourceNotFound',
                'message': 'Requested resource group does not exist'
            }
        }, 404)


@rg.route('/<subId>/resourcegroups/<rgname>', methods=['HEAD'])
def check_existence_resource_group(subId, rgname):
    """
    Checks whether a resource group exists.

    Ref: https://docs.microsoft.com/en-us/rest/api/resources/resource-groups/check-existence
    """
    matches = ResourceGroup.objects.filter(name=rgname, subscription=subId)
    status = 204 if matches.count() > 0 else 404
    return ('', status)


@rg.route('/<subId>/resourcegroups/<rgname>', methods=['PUT'])
def create_or_update_resource_group(subId, rgname):
    """
    Creates or updates a resource group.

    Ref: https://docs.microsoft.com/en-us/rest/api/resources/resource-groups/create-or-update
    """
    try:
        params = request.get_json(force=True)
        params.update({'name': rgname, 'subscription': subId})
        assert params.get('location'), 'Resource group location not specified'

        group = ResourceGroup(**params)
        group.save()
        return jsonify(loads(group.to_json()))
    except AssertionError as err:
        return make_response(jsonify({'error': str(err)}), 400)
    except (ValidationError, FieldDoesNotExist):
        return make_response(jsonify({
            'error': {
                'code': 'ResourceGroupCreationFailed',
                'message': 'Failed to create entity with requested parameters'
            }
        }), 400)


@rg.route('/<subId>/resourcegroups/<rgname>', methods=['DELETE'])
def delete_resource_group(subId, rgname):
    """
    Deletes a resource group.

    Ref: https://docs.microsoft.com/en-us/rest/api/resources/resource-groups/delete
    """
    try:
        group = ResourceGroup.objects.get(name=rgname, subscription=subId)
        group.delete()
    except ResourceGroup.DoesNotExist:
        pass
    return jsonify()


@rg.route('/<subId>/resourcegroups/<rgname>', methods=['PATCH'])
def update_resource_group(subId, rgname):
    """
    Updates a resource group.

    Ref: https://docs.microsoft.com/en-us/rest/api/resources/resource-groups/update
    """
    try:
        params = request.get_json(force=True)
        group = ResourceGroup.objects.get(name=rgname, subscription=subId)
        group.name = params.get('name', group.name)
        group.tags = params.get('tags', group.tags)
        group.managedBy = params.get('managedBy', group.managedBy)
        group.properties = params.get('properties', group.properties)
        group.save()
    except ResourceGroup.DoesNotExist:
        return make_response({
            'error': {
                'code': 'ResourceNotFound',
                'message': 'Requested resource group does not exist'
            }
        }, 404)
    return jsonify(loads(group.to_json()))
