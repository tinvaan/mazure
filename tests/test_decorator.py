
import uuid
import secrets
import unittest

from werkzeug.routing import Map
from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ResourceNotFoundError

from mazure import mazure
from mazure.services import app


class TestMazureDecorator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = str(uuid.uuid4())
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = StorageManagementClient(cls.creds, cls.subscription)

    @mazure
    def test_plain_decorator(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )

    @mazure()
    def test_empty_decorator(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )

    @mazure('storage')
    def test_module_arg_decorator(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )

    @mazure('storage_accounts')
    def test_module_property_arg_decorator(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )

    @mazure('compute')
    def test_invalid_arg_decorator(self):
        with self.assertRaises(NotImplementedError):
            self.assertListEqual(
                [], [_ for _ in self.client.storage_accounts.list()]
            )

    @mazure('storage', allow=True)
    def test_invalid_arg_with_passthru(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )
        with self.assertRaises(ResourceNotFoundError):
            client = ComputeManagementClient(self.creds, self.subscription)
            self.assertEqual(
                [], [_ for _ in client.virtual_machines.list_all()])

    @mazure('storage_accounts', allow=True)
    def test_args_kwargs_decorator(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )
        with self.assertRaises(ResourceNotFoundError):
            client = ComputeManagementClient(self.creds, self.subscription)
            self.assertEqual(
                [], [_ for _ in client.virtual_machines.list_all()])

    def tearDown(self):
        app.url_map = Map()
        app.blueprints.clear()
        app.config.update({'ALLOW_AZURE_REQUESTS': False})


if __name__ == '__main__':
    unittest.main()
