
import os
import uuid

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient

from mazure.proxy import AzureProxy
from mazure.services.storageaccounts.models import StorageAccount
from mazure.services.virtualmachines.models import VirtualMachine


group = 'testrg'
subscription = str(uuid.uuid4())
vms = [
    {
        'name': 'first-vm',
        'location': 'eastus',
        'subscription': subscription,
        'resourceGroup': group
    },
    {
        'name': 'second-vm',
        'location': 'eastus',
        'subscription': subscription,
        'resourceGroup': group
    }
]
accounts = [
    {
        'name': 'first',
        'location': 'eastus',
        'subscription': subscription,
        'resourceGroup': group
    },
    {
        'name': 'second',
        'location': 'westus',
        'subscription': subscription,
        'resourceGroup': group
    },
    {
        'name': 'third',
        'location': 'centralindia',
        'subscription': subscription,
        'resourceGroup': group
    }
]


def before_all(context):
    context.clients = dict()
    context.proxy = AzureProxy()
    creds = ClientSecretCredential(
        tenant_id=os.environ.get('AZURE_TENANT_ID'),
        client_id=os.environ.get('AZURE_CLIENT_ID'),
        client_secret=os.environ.get('AZURE_SECRET_KEY'))

    context.rgroup = group
    context.subscription = subscription
    context.clients.update({
        'sa': StorageManagementClient(creds, subscription),
        'vm': ComputeManagementClient(creds, subscription)
    })


def before_scenario(context, scenario):
    for vm in vms:
        VirtualMachine(**vm).save()
    for account in accounts:
        StorageAccount(**account).save()


def after_scenario(context, scenario):
    VirtualMachine.objects.delete()
    StorageAccount.objects.delete()
