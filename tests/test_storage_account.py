
import os
import vcr
import unittest

from bson import ObjectId

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient


class TestStorageAccounts(unittest.TestCase):
    @vcr.use_cassette('/tmp/azure/auth.yaml')
    def setUp(self):
        self.creds = ClientSecretCredential(
            tenant_id=os.environ.get('AZURE_TENANT_ID'),
            client_id=os.environ.get('AZURE_CLIENT_ID'),
            client_secret=os.environ.get('AZURE_SECRET_KEY'))
        self.assertIsNotNone(self.creds)

    @vcr.use_cassette('/tmp/azure/sa.yaml')
    def test_list_storage_accounts(self):
        client = StorageManagementClient(
            self.creds, os.environ.get('AZURE_SUBSCRIPTION_ID'))
        for account in client.storage_accounts.list():
            print('\n', account, '\n')

    @vcr.use_cassette('/tmp/azure/sa.rg.yml')
    def test_list_storage_accounts_by_rg(self):
        client = StorageManagementClient(
            self.creds, os.environ.get('AZURE_SUBSCRIPTION_ID'))
        for account in client.storage_accounts.list_by_resource_group('rampup'):
            print('\n', account)


if __name__ == '__main__':
    unittest.main()
