
import uuid
import secrets
import unittest

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ResourceNotFoundError

from mazure import mazure
from mazure.proxy import AzureProxy
from mazure.services.virtualmachines.models import VirtualMachine


subscription = str(uuid.uuid4())
vms = [
    {
        'name': 'first-vm',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': subscription
    },
    {
        'name': 'second-vm',
        'location': 'eastus',
        'resourceGroup': 'testrg',
        'subscription': subscription
    }
]


class TestVirtualMachineProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = subscription
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = ComputeManagementClient(cls.creds, cls.subscription)

    def setUp(self):
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
                self.assertEqual(vm.subscription, self.subscription)

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


class TestVirtualMachineProxyDecorator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = subscription
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = ComputeManagementClient(cls.creds, cls.subscription)

    def setUp(self):
        for vm in vms:
            VirtualMachine(**vm).save()

    @mazure
    def test_get_vm_info(self):
        vm = self.client.virtual_machines.get(
            resource_group_name='testrg', vm_name='first-vm')
        self.assertIsNotNone(vm)
        with self.assertRaises(ResourceNotFoundError):
            self.client.virtual_machines.get(
                resource_group_name='testrg', vm_name='third-vm')

    @mazure
    @unittest.skip("FIXME: Raises a ClientAuthentication error")
    def test_get_vm_instance_view(self):
        vm = self.client.virtual_machines.instance_view(
            resource_group_name='testrg', vm_name='first-vm')
        self.assertIsNotNone(vm)
        with self.assertRaises(ResourceNotFoundError):
            self.client.virtual_machines.instance_view(
                resource_group_name='newrg', vm_name='first-vm')

    @mazure
    def test_list_all_vms(self):
        machines = self.client.virtual_machines.list_all()
        self.assertEqual(len(list(machines)), 2)
        for vm in machines:
            self.assertEqual(vm.subscription, self.subscription)

    @mazure
    def test_list_vms_per_rg(self):
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
