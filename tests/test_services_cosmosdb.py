
import unittest

from mongoengine import get_db, connect, disconnect

from .loader import Env
from mazure.services import app
from mazure.services.utils import register, services
from mazure.services.cosmosdb.models import DatabaseAccount


accounts = [
    {
        'name': 'ddb1',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': 'testapp'
    },
    {
        'name': 'ddb2',
        'location': 'westus',
        'resourceGroup': 'testrg',
        'subscription': 'testapp'
    }
]


class TestCosmosDBService(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register(app, services(app, ['cosmosdb']))
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.conn = connect(
            alias=app.config.get('RESOURCE_TYPE_COSMOSDB', 'cosmosdb'),
            db=app.config.get('MAZURE_RESOURCE_MODEL', 'test'),
            host='mongomock://localhost')

    def setUp(self):
        self.env = Env.load()
        self.db = get_db('cosmosdb')
        self.url = self.env.host + '/dbs'
        for params in accounts:
            DatabaseAccount(**params).save()

    def test_list_databases(self):
        r = self.app.get(self.url + '/')
        self.assertEqual(r.status_code, 200)

    def test_create_database(self):
        r = self.app.post(self.url + '/', json={'id': 'ddb3'})
        self.assertEqual(r.status_code, 200)

    def tearDown(self):
        self.db.drop_collection('cosmosdb')
        self.db.client.drop_database(self.db.name)

    @classmethod
    def tearDownClass(cls):
        disconnect(app.config.get('RESOURCE_TYPE_COSMOSDB', 'cosmosdb'))


if __name__ == '__main__':
    unittest.main()
