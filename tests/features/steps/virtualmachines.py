
from behave import given, then
from azure.core.exceptions import ResourceNotFoundError

from mazure.services.virtualmachines.models import VirtualMachine


@given('Virtual machines are not present in a subscription')
def step_impl(context):
    VirtualMachine.objects(subscription=context.subscription).delete()


@given('Virtual machines are present in a subscription')
def step_impl(context):
    vms = VirtualMachine.objects.filter(subscription=context.subscription)
    if vms.count() == 0:
        for vm in VirtualMachine.objects.all():
            vm.subscription = context.subscription
            vm.save()


@given('Virtual machines are not present in a resource group')
def step_impl(context):
    VirtualMachine.objects(resourceGroup=context.rgroup).delete()


@given('Virtual machines are present in a resource group')
def step_impl(context):
    vms = VirtualMachine.objects.filter(resourceGroup=context.rgroup)
    if vms.count() == 0:
        for vm in VirtualMachine.objects.all():
            vm.resourceGroup = context.rgroup
            vm.save()


@given('New virtual machine with name "{vmName}" is created')
@when('New virtual machine with name "{vmName}" is created')
def step_impl(context, vmName):
    client = context.clients.get('vm')
    with context.proxy:
        vmParams = {
            "location": "eastus",
            "storage_profile": {
                "image_reference": {
                    "publisher": 'Canonical',
                    "offer": "UbuntuServer",
                    "sku": "16.04.0-LTS",
                    "version": "latest"
                }
            },
            "hardware_profile": {
                "vm_size": "Standard_DS1_v2"
            },
            "os_profile": {
                "computer_name": "test-pc",
                "admin_username": "foo",
                "admin_password": "bar"
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": f"/subscriptions/{context.subscription}/resourceGroups/{context.rgroup}/providers/Microsoft.Network/networkInterfaces/test-nic",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            }
        }
        try:
            context.response = client\
                .virtual_machines\
                .begin_create_or_update(context.rgroup, vmName, vmParams)
        except Exception:
            context.error = True


@given('Virtual machines are queried in the subscription')
def step_impl(context):
    client = context.clients.get('vm')
    with context.proxy:
        context.response = client.virtual_machines.list_all()


@given('Virtual machines are queried in the resource group')
def step_impl(context):
    client = context.clients.get('vm')
    with context.proxy:
        context.response = client.virtual_machines.list(context.rgroup)


@given('Virtual machine with name "{vmName}" is queried')
@when('Virtual machine with name "{vmName}" is queried')
def step_impl(context, vmName):
    client = context.clients.get('vm')
    with context.proxy:
        try:
            context.response = client.virtual_machines\
                                     .get(context.rgroup, vmName)
        except ResourceNotFoundError:
            context.error = True


@then('Virtual machine with name "{vmName}" is deleted')
@given('Virtual machine with name "{vmName}" is deleted')
def step_impl(context, vmName):
    client = context.clients.get('vm')
    with context.proxy:
        try:
            context.response = client.virtual_machines\
                                     .begin_delete(context.rgroup, vmName)
        except ResourceNotFoundError:
            context.error = True


@then('Return an empty list of virtual machines')
def step_impl(context):
    with context.proxy:
        assert len([item for item in context.response]) == 0


@then('Return a list of existing virtual machines')
def step_impl(context):
    with context.proxy:
        assert len([item for item in context.response]) > 0


@then('Return information for virtual machine with name "{vmName}"')
def step_impl(context, vmName):
    assert context.response.name == vmName


@then('Raise an exception')
@then('Raise a ResourceNotFoundError')
@then('Virtual machine is silently deleted')
def step_impl(context):
    assert (
        context.error if hasattr(context, 'error')
        else context.response.status() == 'Succeeded'
    )
