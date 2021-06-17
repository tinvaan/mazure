
import uuid
import secrets
import unittest

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    StorageAccountCheckNameAvailabilityParameters
)

from mazure import mazure
from mazure.proxy import AzureProxy
from mazure.services.storageaccounts.models import StorageAccount


group = 'testrg'
subscription = str(uuid.uuid4())
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


class TestStorageAccountProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = subscription
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = StorageManagementClient(cls.creds, cls.subscription)

    def setUp(self):
        for account in accounts:
            StorageAccount(**account).save()

    def test_list_storage_accounts(self):
        with AzureProxy():
            sas = self.client.storage_accounts.list()
            self.assertEqual(len([sa for sa in sas]), 3)
            for sa in sas:
                self.assertIsNotNone(sa)

    def test_check_storage_account_name(self):
        valid = StorageAccountCheckNameAvailabilityParameters(name='foobarsa')
        invalid = StorageAccountCheckNameAvailabilityParameters(name='testkit')
        with AzureProxy():
            self.assertTrue(self.client.storage_accounts
                            .check_name_availability(valid).name_available)
            self.assertTrue(self.client.storage_accounts
                            .check_name_availability(invalid).name_available)

    def test_create_storage_account(self):
        with AzureProxy():
            kws = {
                "sku": {"name": "Premium_LRS"},
                "kind": "BlockBlobStorage",
                "location": "eastus",
            }
            self.client.storage_accounts.begin_create(
                'testrg', 'testaccount', StorageAccountCreateParameters(**kws))
            self.assertIsNotNone(
                StorageAccount.objects.get(name='testaccount'))

            with self.assertRaises(Exception):
                self.client.storage_accounts.begin_create(
                    'testrg', 'testaccount', StorageAccountCreateParameters(**kws))
                self.assertEqual(StorageAccount.objects(
                    resourceGroup='testrg', name='testaccount').count(), 1)

    def test_delete_storage_account(self):
        with AzureProxy():
            self.client.storage_accounts.delete(
                account_name='testaccount', resource_group_name='testrg')
            self.assertEqual(StorageAccount.objects(
                resourceGroup='testrg', name='testaccount').count(), 0)

            # TODO: Should this fail silently?
            self.client.storage_accounts.delete(
                account_name='nonexistent', resource_group_name='testrg')
            self.assertEqual(StorageAccount.objects(
                resourceGroup='testrg', name='nonexistent').count(), 0)

    def tearDown(self):
        StorageAccount.objects.delete()


class TestStorageAccountProxyDecorator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = subscription
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = StorageManagementClient(cls.creds, cls.subscription)

    def setUp(self):
        for account in accounts:
            StorageAccount(**account).save()

    @mazure
    def test_list_storage_accounts(self):
        sas = self.client.storage_accounts.list()
        self.assertEqual(len([sa for sa in sas]), 3)
        for sa in sas:
            self.assertIsNotNone(sa)

    @mazure
    def test_check_storage_account_name(self):
        valid = StorageAccountCheckNameAvailabilityParameters(name='foobarsa')
        invalid = StorageAccountCheckNameAvailabilityParameters(name='testkit')
        self.assertTrue(self.client.storage_accounts
                        .check_name_availability(valid).name_available)
        self.assertTrue(self.client.storage_accounts
                        .check_name_availability(invalid).name_available)

    @mazure
    def test_create_storage_account(self):
        kws = {
            "sku": {"name": "Premium_LRS"},
            "kind": "BlockBlobStorage",
            "location": "eastus",
        }
        self.client.storage_accounts.begin_create(
            'testrg', 'testaccount', StorageAccountCreateParameters(**kws))
        self.assertIsNotNone(
            StorageAccount.objects.get(name='testaccount'))

        with self.assertRaises(Exception):
            self.client.storage_accounts.begin_create(
                'testrg', 'testaccount', StorageAccountCreateParameters(**kws))
            self.assertEqual(StorageAccount.objects(
                resourceGroup='testrg', name='testaccount').count(), 1)

    @mazure
    def test_delete_storage_account(self):
        self.client.storage_accounts.delete(
            account_name='testaccount', resource_group_name='testrg')
        self.assertEqual(StorageAccount.objects(
            resourceGroup='testrg', name='testaccount').count(), 0)

        # TODO: Should this fail silently?
        self.client.storage_accounts.delete(
            account_name='nonexistent', resource_group_name='testrg')
        self.assertEqual(StorageAccount.objects(
            resourceGroup='testrg', name='nonexistent').count(), 0)

    def tearDown(self):
        StorageAccount.objects.delete()


if __name__ == '__main__':
    unittest.main()
