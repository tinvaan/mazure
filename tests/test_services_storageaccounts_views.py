
import unittest

from mongoengine import get_db, connect, disconnect

from .loader import Env
from mazure.services import app
from mazure.services.utils import register, services
from mazure.services.storageaccounts.models import StorageAccount


class TestStorageAccountViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register(app, services(app, ['storage']))
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.conn = connect(
            alias=app.config.get('RESOURCE_TYPE_SA', 'sa'),
            db=app.config.get('MAZURE_RESOURCE_MODEL', 'test'),
            host='mongomock://localhost')

    def setUp(self):
        self.env = Env.load()
        self.db = get_db('sa')
        self.provider = 'providers/Microsoft.Storage/storageAccounts'
        self.url = self.env.host + '/subscriptions/%s' % self.env.subscription

    def test_list_storage_accounts(self):
        r = self.app.get('%s/%s' % (self.url, self.provider))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            len(StorageAccount.objects.all()), len(r.get_json().get('value')))

    def test_check_storage_account_name(self):
        url = '%s/%s' % (
            self.url,
            self.provider.replace('storageAccounts', 'checkNameAvailability'))

        r = self.app.post(url)
        self.assertEqual(r.status_code, 400)

        r = self.app.post(url, json={'name': 'foobar'})
        self.assertEqual(r.status_code, 400)

        r = self.app.post(url, json={
            'name': 'foobar', 'type': 'Microsoft.Storage/storageAccounts'})
        self.assertEqual(r.status_code, 200)

    def test_create_storage_account(self):
        r = self.app.put(
            '%s/resourceGroups/testrg/%s/testsa' % (self.url, self.provider))
        self.assertEqual(r.status_code, 400)

        r = self.app.put(
            '%s/resourceGroups/testrg/%s/testsa' % (self.url, self.provider),
            json={
                'kind': 'BlockBlobStorage',
                'sku': {'name': 'Premium_SA'},
                'location': 'eastus'
            })
        self.assertEqual(r.status_code, 200)

    def test_delete_storage_account(self):
        pass

    def tearDown(self):
        self.db.drop_collection('resources')
        self.db.client.drop_database(self.db.name)

    @classmethod
    def tearDownClass(cls):
        disconnect(app.config.get('RESOURCE_TYPE_SA', 'sa'))


if __name__ == '__main__':
    unittest.main()
