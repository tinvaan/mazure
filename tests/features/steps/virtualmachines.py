
from behave import given, then

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


@then('Return an empty list of virtual machines')
def step_impl(context):
    with context.proxy:
        print(context.response)
        assert len([item for item in context.response]) == 0


@then('Return a list of existing virtual machines')
def step_impl(context):
    with context.proxy:
        print(context.response)
        print(context.subscription, VirtualMachine.objects.all())
        assert len([item for item in context.response]) > 0
