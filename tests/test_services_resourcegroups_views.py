
import unittest

from mongoengine import get_db, connect, disconnect

from .loader import Env
from mazure.services import app
from mazure.services.utils import register, services
from mazure.services.resourcegroups.models import ResourceGroup


groups = [
    {
        "name": "rg1",
        "location": "eastus",
        "subscription": "testapp"
    },
    {
        "name": "rg2",
        "location": "westus",
        "subscription": "testapp"
    }
]


class TestResourceGroupViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register(app, services(app, ['resources']))
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.conn = connect(
            host='mongomock://localhost',
            alias=app.config.get('RESOURCE_TYPE_RG', 'rg'),
            db=app.config.get('MAZURE_RESOURCE_MODEL', 'test'))

    def setUp(self):
        self.env = Env.load()
        self.db = get_db('rg')
        self.url = '%s/subscriptions/%s/resourcegroups' \
            % (self.env.host, self.env.subscription)
        for args in groups:
            ResourceGroup(**args).save()

    def test_get_resource_group(self):
        r = self.app.get(self.url + '/foo')
        self.assertEqual(r.status_code, 404)

        for group in groups:
            r = self.app.get(self.url + '/' + group.get('name'))
            self.assertEqual(r.status_code, 200)

    def test_list_resource_groups(self):
        r = self.app.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_create_resource_group(self):
        with self.assertRaises(ResourceGroup.DoesNotExist):
            ResourceGroup.objects.get(name='testrg')

        params = {
            'location': 'eastus',
            'tags': {
                'name': 'testrg',
                'purpose': 'testing'
            }
        }
        r = self.app.put(self.url + '/testrg', json=params)
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(ResourceGroup.objects.get(name='testrg'))

    def test_delete_resource_group(self):
        r = self.app.delete(self.url + '/foo')
        self.assertEqual(r.status_code, 200)

        self.assertIsNotNone(ResourceGroup.objects.get(name='rg1'))
        r = self.app.delete(self.url + '/rg1')
        self.assertEqual(r.status_code, 200)
        with self.assertRaises(ResourceGroup.DoesNotExist):
            ResourceGroup.objects.get(name='rg1')

    def tearDown(self):
        self.db.drop_collection('resourcegroups')
        self.db.client.drop_database(self.db.name)

    @classmethod
    def tearDownClass(cls):
        disconnect(app.config.get('RESOURCE_TYPE_RG', 'rg'))


if __name__ == '__main__':
    unittest.main()
