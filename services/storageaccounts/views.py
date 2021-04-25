
from . import sa


prefix = '/<subId>/resourceGroups/<rgroup>'
provider = '/providers/Microsoft.Storage/storageAccounts'


@sa.route('/<subId>' + provider)
def list_storage_accounts(subId):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/list
    """


@sa.route('/<subId>' + provider.replace('storageAccounts', 'checkNameAvailability'))
def check_storage_account_name(subId):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/checknameavailability
    """


@sa.route('%s/%s/<accountName>' % (prefix, provider))
def create_storage_account(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/create
    """


@sa.route('%s/%s/<accountName>' % (prefix, provider))
def delete_storage_account(subId, rgroup, accountName):
    """
    TODO

    Ref: https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/delete
    """


@sa.route('%s/%s/<accountName>/failover' % (prefix, provider))
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
