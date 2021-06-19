
import uuid
import secrets
import unittest

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import ClientAuthenticationError

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

    @mazure('compute', allow=True)
    def test_invalid_arg_with_passthru(self):
        with self.assertRaises(ClientAuthenticationError):
            self.assertListEqual(
                [], [_ for _ in self.client.storage_accounts.list()]
            )

    @mazure('storage_accounts', allow=True, version='2021-01-01')
    def test_args_kwargs_decorator(self):
        self.assertListEqual(
            [], [_ for _ in self.client.storage_accounts.list()]
        )

    def tearDown(self):
        app.config.update({'ALLOW_AZURE_REQUESTS': False})


if __name__ == '__main__':
    unittest.main()
