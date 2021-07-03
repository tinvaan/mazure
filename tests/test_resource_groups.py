
import uuid
import secrets
import unittest

from azure.identity import ClientSecretCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroupPatchable
from azure.mgmt.resource.resources.models import ResourceGroup as AzureResourceGroup
from azure.mgmt.resource.resources.models import ResourceGroupProperties as Properties

from mazure import mazure, Mazure
from mazure.services.resourcegroups.models import ResourceGroup


subscription = str(uuid.uuid4())
groups = [
    {
        "name": "rg1",
        "location": "eastus",
        "subscription": subscription
    },
    {
        "name": "rg2",
        "location": "westus",
        "subscription": subscription
    },
    {
        "name": "rg3",
        "location": "centralindia",
        "subscription": subscription
    }
]


class TestResourceGroupProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = subscription
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = ResourceManagementClient(cls.creds, cls.subscription)

    def setUp(self):
        for args in groups:
            ResourceGroup(**args).save()

    def test_begin_delete(self):
        self.assertIsNotNone(ResourceGroup.objects.get(name='rg3'))
        with Mazure():
            self.client.resource_groups.begin_delete('foobar')
            self.client.resource_groups.begin_delete('rg3')
            with self.assertRaises(ResourceGroup.DoesNotExist):
                ResourceGroup.objects.get(name='rg3')

    @unittest.skip('FIXME')
    def test_check_existence(self):
        with Mazure():
            self.assertFalse(
                self.client.resource_groups.check_existence('foobar'))
            for group in groups:
                self.assertTrue(
                    self.client.resource_groups
                        .check_existence(group.get('name')))

    def test_create_or_update(self):
        with Mazure():
            params = AzureResourceGroup(location='westus')
            rg = self.client.resource_groups.create_or_update('foobar', params)
            self.assertEqual(rg.name, 'foobar')
            self.assertEqual(rg.location, 'westus')
            self.assertEqual(rg.managed_by, self.subscription)

            manager = str(uuid.uuid4())
            params = AzureResourceGroup(
                tags={},
                location='eastus',
                managed_by=manager,
                properties=Properties(provisioning_state='Succeeded')
            )
            rg = self.client.resource_groups.create_or_update('newrg', params)
            self.assertEqual(rg.name, 'newrg')
            self.assertEqual(rg.location, 'eastus')
            self.assertEqual(rg.managed_by, manager)

    def test_get_resource_group(self):
        keys = ['name', 'type', 'properties', 'location', 'managed_by', 'tags']
        with Mazure():
            group = self.client.resource_groups.get('rg1')
            self.assertListEqual(list(group.as_dict().keys()), keys)
            with self.assertRaises(ResourceNotFoundError):
                self.client.resource_groups.get('foobar')

    def test_list_resource_groups(self):
        with Mazure():
            self.assertListEqual(
                [group['name'] for group in groups],
                [group.name for group in self.client.resource_groups.list()]
            )

    def test_update_resource_group(self):
        with Mazure():
            patch = ResourceGroupPatchable(tags={
                'new': 'tag',
                'added': str(True)
            })
            group = self.client.resource_groups.update('rg3', patch)
            self.assertDictEqual(group.tags, patch.tags)
            with self.assertRaises(ResourceNotFoundError):
                self.client.resource_groups.update('foobar', patch)

    def tearDown(self):
        ResourceGroup.objects.delete()


class TestResourceGroupProxyDecorator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = subscription
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = ResourceManagementClient(cls.creds, cls.subscription)

    def setUp(self):
        for args in groups:
            ResourceGroup(**args)

    @mazure
    def test_begin_delete(self):
        self.assertIsNotNone(ResourceGroup.objects.get(name='rg3'))
        self.client.resource_groups.begin_delete('foobar')
        self.client.resource_groups.begin_delete('rg3')
        with self.assertRaises(ResourceGroup.DoesNotExist):
            ResourceGroup.objects.get(name='rg3')

    @mazure
    @unittest.skip('FIXME')
    def test_check_existence(self):
        self.assertFalse(
            self.client.resource_groups.check_existence('foobar'))
        for group in groups:
            self.assertTrue(
                self.client.resource_groups
                    .check_existence(group.get('name')))

    @mazure
    def test_create_or_update(self):
        params = AzureResourceGroup(location='westus')
        rg = self.client.resource_groups.create_or_update('foobar', params)
        self.assertEqual(rg.name, 'foobar')
        self.assertEqual(rg.location, 'westus')
        self.assertEqual(rg.managed_by, self.subscription)

        manager = str(uuid.uuid4())
        params = AzureResourceGroup(
            tags={},
            location='eastus',
            managed_by=manager,
            properties=Properties(provisioning_state='Succeeded')
        )
        rg = self.client.resource_groups.create_or_update('newrg', params)
        self.assertEqual(rg.name, 'newrg')
        self.assertEqual(rg.location, 'eastus')
        self.assertEqual(rg.managed_by, manager)

    @mazure
    def test_get_resource_group(self):
        keys = ['name', 'type', 'properties', 'location', 'managed_by', 'tags']
        group = self.client.resource_groups.get('rg1')
        self.assertListEqual(list(group.as_dict().keys()), keys)
        with self.assertRaises(ResourceNotFoundError):
            self.client.resource_groups.get('foobar')

    @mazure
    def test_list_resource_groups(self):
        self.assertListEqual(
            [group['name'] for group in groups],
            [group.name for group in self.client.resource_groups.list()]
        )

    @mazure
    def test_update_resource_group(self):
        patch = ResourceGroupPatchable(tags={
            'new': 'tag',
            'added': str(True)
        })
        group = self.client.resource_groups.update('rg3', patch)
        self.assertDictEqual(group.tags, patch.tags)
        with self.assertRaises(ResourceNotFoundError):
            self.client.resource_groups.update('foobar', patch)