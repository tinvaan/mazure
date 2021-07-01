
import unittest

from mongoengine import get_db, connect, disconnect

from .loader import Env
from mazure.services import app
from mazure.services.utils import register, services
from mazure.services.virtualmachines.models import VirtualMachine


vms = [
    {
        'name': 'first-vm',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': 'testapp'
    },
    {
        'name': 'second-vm',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': 'testapp'
    }
]


class TestVirtualMachineViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register(app, services(app, ['compute']))
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.conn = connect(
            alias=app.config.get('RESOURCE_TYPE_VM', 'vm'),
            db=app.config.get('MAZURE_RESOURCE_MODEL', 'test'),
            host='mongomock://localhost')

    def setUp(self):
        self.env = Env.load()
        self.db = get_db('vm')
        self.provider = 'providers/Microsoft.Compute/virtualMachines'
        self.url = self.env.host + '/subscriptions/%s' % self.env.subscription
        for vm in vms:
            VirtualMachine(**vm).save()

    def test_get_vm_info(self):
        r = self.app.get(
            '%s/resourceGroups/testrg/%s/sixth-vm' % (self.url, self.provider))
        self.assertEqual(r.status_code, 404)

        r = self.app.get(
            '%s/resourceGroups/rgs/%s/second-vm' % (self.url, self.provider))
        self.assertEqual(r.status_code, 404)

        r = self.app.get(
            '%s/resourceGroups/testrg/%s/first-vm' % (self.url, self.provider))
        self.assertEqual(r.status_code, 200)

    def test_get_vm_instance_view(self):
        r = self.app.get('%s/resourceGroups/testrg/%s/sixth-vm/instanceView'
                         % (self.url, self.provider))
        self.assertEqual(r.status_code, 404)

        r = self.app.get('%s/resourceGroups/rgs/%s/second-vm/instanceView'
                         % (self.url, self.provider))
        self.assertEqual(r.status_code, 404)

        r = self.app.get('%s/resourceGroups/testrg/%s/first-vm/instanceView'
                         % (self.url, self.provider))
        self.assertEqual(r.status_code, 200)

    def test_list_vms_per_rg(self):
        r = self.app.get(
            '%s/resourceGroups/xyz/%s' % (self.url, self.provider))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json().get('value')), 0)

        r = self.app.get(
            '%s/resourceGroups/testrg/%s' % (self.url, self.provider))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json().get('value')), 2)

    def test_list_vms_per_subscription(self):
        r = self.app.get('%s/subscriptions/xyz/%s' % (self.env.host, self.provider))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json().get('value')), 0)

        r = self.app.get('%s/%s' % (self.url, self.provider))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json().get('value')), 2)

    def test_create_or_update(self):
        url = '%s/resourceGroups/testrg/%s/test-vm' % (self.url, self.provider)
        r = self.app.put(url)
        self.assertEqual(r.status_code, 400)

        r = self.app.put(
            url, json={'location': 'eastus', 'tags': [{'foo': 'bar'}]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json().get('name'), 'test-vm')
        self.assertEqual(r.get_json().get('location'), 'eastus')

    def test_delete_vm(self):
        url = '%s/resourceGroups/testrg/%s/foo-vm' % (self.url, self.provider)
        r = self.app.delete(url)
        self.assertEqual(r.status_code, 204)

        url = '%s/resourceGroups/testrg/%s/first-vm' % (self.url, self.provider)
        r = self.app.delete(url)
        self.assertEqual(r.status_code, 200)
        with self.assertRaises(VirtualMachine.DoesNotExist):
            VirtualMachine.objects.get(
                name='first-vm',
                subscription=self.env.subscription,
                resourceGroup=self.env.rgroup)

    def tearDown(self):
        self.db.drop_collection('virtualmachines')
        self.db.client.drop_database(self.db.name)

    @classmethod
    def tearDownClass(cls):
        disconnect(app.config.get('RESOURCE_TYPE_VM', 'sa'))


if __name__ == '__main__':
    unittest.main()
