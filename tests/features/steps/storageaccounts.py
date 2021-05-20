
from behave import given, then
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


@then('Return truthy availability')
def step_impl(context):
    assert context.response.name_available is True


@then('Return falsy availability')
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
