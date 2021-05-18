
import os
import vcr
import unittest

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCheckNameAvailabilityParameters
)

from mazure.proxy import AzureInterceptor as AzureProxy


@unittest.skip('Used for debugging request/responses')
class TestStorageAccounts(unittest.TestCase):
    @vcr.use_cassette('/tmp/azure/auth.yaml')
    @classmethod
    def setUpClass(cls):
        cls.creds = ClientSecretCredential(
            tenant_id=os.environ.get('AZURE_TENANT_ID'),
            client_id=os.environ.get('AZURE_CLIENT_ID'),
            client_secret=os.environ.get('AZURE_SECRET_KEY'))
        cls.client = StorageManagementClient(
            cls.creds, os.environ.get('AZURE_SUBSCRIPTION_ID'))

    def setUp(self):
        self.assertIsNotNone(self.creds)
        self.assertIsNotNone(self.client)

    @vcr.use_cassette('/tmp/azure/sa.name.yaml')
    def test_check_storage_account_name(self):
        valid = StorageAccountCheckNameAvailabilityParameters(name='foobarsa')
        invalid = StorageAccountCheckNameAvailabilityParameters(name='rampupsa')
        self.assertTrue(self.client.storage_accounts
                        .check_name_availability(valid).name_available)
        self.assertFalse(self.client.storage_accounts
                         .check_name_availability(invalid).name_available)

    @vcr.use_cassette('/tmp/azure/sa.yaml')
    def test_list_storage_accounts(self):
        for account in self.client.storage_accounts.list():
            self.assertIsNotNone(account)

    @vcr.use_cassette('/tmp/azure/sa.rg.yml')
    def test_list_storage_accounts_by_rg(self):
        for account in self.client.storage_accounts.list_by_resource_group('rampup'):
            self.assertIsNotNone(account)


class TestStorageAccountProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.creds = ClientSecretCredential(
            tenant_id=os.environ.get('AZURE_TENANT_ID'),
            client_id=os.environ.get('AZURE_CLIENT_ID'),
            client_secret=os.environ.get('AZURE_SECRET_KEY'))
        cls.client = StorageManagementClient(
            cls.creds, os.environ.get('AZURE_SUBSCRIPTION_ID'))

    def setUp(self):
        self.assertIsNotNone(self.creds)
        self.assertIsNotNone(self.client)

    def test_list_storage_accounts(self):
        with AzureProxy():
            for account in self.client.storage_accounts.list():
                self.assertIsNotNone(account)

    def test_check_storage_account_name(self):
        valid = StorageAccountCheckNameAvailabilityParameters(name='foobarsa')
        invalid = StorageAccountCheckNameAvailabilityParameters(name='rampupsa')
        with AzureProxy():
            self.assertTrue(self.client.storage_accounts
                            .check_name_availability(valid).name_available)
            self.assertTrue(self.client.storage_accounts
                            .check_name_availability(invalid).name_available)


if __name__ == '__main__':
    unittest.main()
