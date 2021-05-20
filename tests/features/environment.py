
from mazure.services.storageaccounts.models import StorageAccount
import os

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient

from mazure.proxy import AzureProxy
from mazure.services.storageaccounts.models import StorageAccount


accounts = [
    {
        'name': 'first',
        'location': 'eastus',
        'subscription': os.environ.get('AZURE_SUBSCRIPTION_ID'),
        'resourceGroup': 'testrg'
    },
    {
        'name': 'second',
        'location': 'westus',
        'subscription': os.environ.get('AZURE_SUBSCRIPTION_ID'),
        'resourceGroup': 'testrg'
    },
    {
        'name': 'third',
        'location': 'centralindia',
        'subscription': os.environ.get('AZURE_SUBSCRIPTION_ID'),
        'resourceGroup': 'testrg'
    }
]


def before_all(context):
    context.clients = dict()
    context.proxy = AzureProxy()
    creds = ClientSecretCredential(
        tenant_id=os.environ.get('AZURE_TENANT_ID'),
        client_id=os.environ.get('AZURE_CLIENT_ID'),
        client_secret=os.environ.get('AZURE_SECRET_KEY'))

    context.clients.update({
        'sa': StorageManagementClient(creds, os.environ.get('AZURE_SUBSCRIPTION_ID'))
    })


def before_scenario(context, scenario):
    for params in accounts:
        StorageAccount(**params).save()


def after_scenario(context, scenario):
    StorageAccount.objects.delete()
