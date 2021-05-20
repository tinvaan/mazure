
from behave import given, then, when
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    StorageAccountCheckNameAvailabilityParameters
)

from mazure.services.storageaccounts.models import StorageAccount


@given('Storage accounts are setup')
def step_impl(context):
    pass


@given('Storage accounts are not setup')
def step_impl(context):
    StorageAccount.objects.delete()


@given('New storage account name is requested')
def step_impl(context):
    client = context.clients.get('sa')
    with context.proxy:
        name = StorageAccountCheckNameAvailabilityParameters(name='fourth')
        context.response = client.storage_accounts.check_name_availability(name)


@given('Existing storage account name is requested')
def step_impl(context):
    client = context.clients.get('sa')
    with context.proxy:
        name = StorageAccountCheckNameAvailabilityParameters(name='second')
        context.response = client.storage_accounts.check_name_availability(name)


@given('Storage accounts are queried')
def step_impl(context):
    client = context.clients.get('sa')
    with context.proxy:
        context.response = client.storage_accounts.list()


@given('Storage account with name "{}" is deleted')
def step_impl(context, name):
    client = context.clients.get('sa')
    with context.proxy:
        context.response = client.storage_accounts.delete(
            account_name=name, resource_group_name='testrg')
    context.name = name


@when('New storage account is created with name "{name}"')
def step_impl(context, name):
    kws = {
        'sku': {'name': 'Premium_LRS'},
        'kind': 'BlockBlobStorage',
        'location': 'westus'
    }
    client = context.clients.get('sa')
    with context.proxy:
        try:
            context.response = client.storage_accounts.begin_create(
                'testrg', name, StorageAccountCreateParameters(**kws))
        except Exception:
            context.error = True
    context.name = name


@then('Storage account name is available')
@given('Storage account name is available')
def step_impl(context):
    assert context.response.name_available is True


@then('Storage account name is unavailable')
@given('Storage account name is unavailable')
def step_impl(context):
    assert context.response.name_available is False


@then('Return an empty list of storage accounts')
def step_impl(context):
    with context.proxy:
        assert len(list(context.response)) == 0


@then('Return a list of existing storage accounts')
def step_impl(context):
    with context.proxy:
        for account in context.response:
            assert account


@then('Requested name is found in list of storage accounts')
def step_impl(context):
    client = context.clients.get('sa')
    with context.proxy:
        assert context.name in [
            account.name for account in client.storage_accounts.list()]


@then('Create operation raises an error')
def step_impl(context):
    assert context.error is True


@then('Deleted account is not found in list of storage accounts')
def step_impl(context):
    client = context.clients.get('sa')
    with context.proxy:
        assert context.name not in [
            account.name for account in client.storage_accounts.list()]


@then('List of storage accounts is unchanged')
def step_impl(context):
    client = context.clients.get('sa')
    with context.proxy:
        assert ['first', 'second', 'third'] == [
            account.name for account in client.storage_accounts.list()]