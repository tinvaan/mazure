
import os
import unittest

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ResourceNotFoundError

from mazure.proxy import AzureProxy
from mazure.services.virtualmachines.models import VirtualMachine


vms = [
    {
        'name': 'first-vm',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': os.environ.get('AZURE_SUBSCRIPTION_ID')
    },
    {
        'name': 'second-vm',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': os.environ.get('AZURE_SUBSCRIPTION_ID')
    }
]


class TestVirtualMachineProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.creds = ClientSecretCredential(
            tenant_id=os.environ.get('AZURE_TENANT_ID'),
            client_id=os.environ.get('AZURE_CLIENT_ID'),
            client_secret=os.environ.get('AZURE_SECRET_KEY'))
        cls.client = ComputeManagementClient(
            cls.creds, os.environ.get('AZURE_SUBSCRIPTION_ID'))

    def setUp(self):
        self.assertIsNotNone(self.creds)
        self.assertIsNotNone(self.client)
        for vm in vms:
            VirtualMachine(**vm).save()

    def test_get_vm_info(self):
        with AzureProxy():
            vm = self.client.virtual_machines.get(
                resource_group_name='testrg', vm_name='first-vm')
            self.assertIsNotNone(vm)
            with self.assertRaises(ResourceNotFoundError):
                self.client.virtual_machines.get(
                    resource_group_name='testrg', vm_name='third-vm')

    @unittest.skip("FIXME: Raises a ClientAuthentication error")
    def test_get_vm_instance_view(self):
        vm = self.client.virtual_machines.instance_view(
            resource_group_name='testrg', vm_name='first-vm')
        self.assertIsNotNone(vm)
        with self.assertRaises(ResourceNotFoundError):
            self.client.virtual_machines.instance_view(
                resource_group_name='newrg', vm_name='first-vm')

    def test_list_all_vms(self):
        with AzureProxy():
            machines = self.client.virtual_machines.list_all()
            self.assertEqual(len(list(machines)), 2)
            for vm in machines:
                self.assertEqual(
                    vm.subscription, os.environ.get('AZURE_SUBSCRIPTION_ID'))

    def test_list_vms_per_rg(self):
        with AzureProxy():
            machines = self.client.virtual_machines\
                                  .list(resource_group_name='xyz')
            self.assertEqual(len(list(machines)), 0)

            machines = self.client.virtual_machines\
                                  .list(resource_group_name='testrg')
            self.assertEqual(len(list(machines)), 2)
            for vm in machines:
                self.assertEqual(vm.resource_group_name, 'testrg')

    def tearDown(self):
        VirtualMachine.objects.delete()


if __name__ == '__main__':
    unittest.main()
