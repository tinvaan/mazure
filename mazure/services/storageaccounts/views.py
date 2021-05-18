
from .models import StorageAccount

from json import loads
from flask import Blueprint, request, jsonify, make_response
from mongoengine.errors import ValidationError, FieldDoesNotExist


prefix = '/<subId>/resourceGroups/<rgroup>'
provider = '/providers/Microsoft.Storage/storageAccounts'

sa = Blueprint('storageaccounts', __name__)


@sa.route('/<subId>' + provider)
def list_storage_accounts(subId):
    """
    Lists all the storage accounts available under the subscription.

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/list
    """
    values = []
    for account in StorageAccount.objects.filter(subscription=subId):
        values.append({
            'sku': account.sku,
            'kind': account.kind,
            'id': account.rid,
            'name': account.name,
            'type': account.type,
            'location': account.location,
            'tags': account.tags,
            'properties': account.properties
        })
    return jsonify({'value': values})


@sa.route('/<subId>' + provider.replace('storageAccounts', 'checkNameAvailability'), methods=['POST'])
def check_storage_account_name(subId):
    """
    Checks that the storage account name is valid and is not already in use.

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/checknameavailability
    """
    try:
        params = request.get_json(force=True)
        assert params.get('name'), 'Missing required parameter "name"'
        assert params.get('type'), 'Missing required parameter "type"'
        if StorageAccount.objects.filter(
            subscription=subId, name=params.get('name'), type=params.get('type')
        ).count() == 0:
            return jsonify({'nameAvailable': True})
        return jsonify({
            'nameAvailable': False,
            'reason': 'AlreadyExists',
            'message': 'The storage account named rampupsa is already taken.'
        })
    except AssertionError as err:
        return make_response(jsonify({'error': str(err)}), 400)


@sa.route('%s/%s/<accountName>' % (prefix, provider), methods=['PUT'])
def create_storage_account(subId, rgroup, accountName):
    """
    Creates a new storage account with the specified parameters.

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/create
    """
    try:
        params = request.get_json(force=True)
        assert params.get('kind'), 'Storage account type not specified'
        assert params.get('location'), 'Storage account location not specified'
        assert params.get('sku'), 'Storage account sku not provided'
        params.update({
            'name': accountName,
            'subscription': subId,
            'resourceGroup': rgroup
        })
        account = StorageAccount(**params)
        account.save()
        return jsonify(loads(account.to_json()))
    except AssertionError as err:
        return make_response(jsonify({'error': str(err)}), 400)
    except (FieldDoesNotExist, ValidationError):
        return make_response(jsonify({
            'error': {
                'code': 'AccountCreationFailed',
                'message': 'Failed to create storage account'
            }
        }), 400)


@sa.route('%s/%s/<accountName>' % (prefix, provider), methods=['DELETE'])
def delete_storage_account(subId, rgroup, accountName):
    """
    Deletes a storage account in Microsoft Azure.

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/delete
    """
    try:
        account = StorageAccount.objects.get(
            subscription=subId, resourceGroup=rgroup, name=accountName)
        account.delete()
    except StorageAccount.DoesNotExist:
        return make_response(jsonify(), 204)
    return jsonify()


@sa.route('%s/%s/<accountName>/failover' % (prefix, provider), methods=['POST'])
def failover_storage_account(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/failover
    """


@sa.route('%s/%s/<accountName>/ListAccountSas' % (prefix, provider))
def list_sas_credentials(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/listaccountsas
    """


@sa.route('%s/%s' % (prefix, provider))
def list_by_resource_group(subId, rgroup):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/listbyresourcegroup
    """


@sa.route('%s/%s/<accountName>/listKeys' % (prefix, provider))
def list_storage_account_keys(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/listkeys
    """


@sa.route('%s/%s/<accountName>/ListServiceSas' % (prefix, provider))
def list_service_sas(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/listservicesas
    """


@sa.route('%s/%s/<accountName>/regenerateKey' % (prefix, provider))
def regenerate_key(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/listservicesas
    """


@sa.route('%s/%s/<accountName>/restoreBlobRanges' % (prefix, provider))
def restore_blob_ranges(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/restoreblobranges
    """


@sa.route('%s/%s/<accountName>/revokeUserDelegationKeys' % (prefix, provider))
def revoke_user_delegation_keys(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/revokeuserdelegationkeys
    """
