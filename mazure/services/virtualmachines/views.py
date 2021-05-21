
from json import loads
from flask import Blueprint, request, jsonify, make_response

from .models import VirtualMachine


prefix = '/<subId>/resourceGroups/<rgroup>'
provider = '/providers/Microsoft.Compute/virtualMachines'

vm = Blueprint('virtualmachines', __name__)


@vm.route('%s/%s/<vmName>' % (prefix, provider))
def get_vm_info(subId, rgroup, vmName):
    """
    Retrieves information about the model view or the instance view of a virtual machine.

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/get
    """
    try:
        machine = VirtualMachine.objects.get(
            name=vmName, subscription=subId, resourceGroup=rgroup)
        return jsonify(loads(machine.to_json()))
    except VirtualMachine.DoesNotExist:
        return make_response(jsonify({
            'error': {
                'code': 'VirtualMachineDoesNotExist',
                'message': 'Requested virtual machine instance was not found'
            }
        }), 404)


@vm.route('%s/%s/<vmName>/instanceView' % (prefix, provider))
def get_vm_instance_view(subId, rgroup, vmName):
    """
    Retrieves information about the run-time state of a virtual machine.

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/instanceview
    """
    # NOTE:
    # For the sake of a mocked response
    # this is the same as the `get_vm_info()` route
    try:
        machine = VirtualMachine.objects.get(
            name=vmName, subscription=subId, resourceGroup=rgroup)
        return jsonify(loads(machine.to_json()))
    except VirtualMachine.DoesNotExist:
        return make_response(jsonify({
            'error': {
                'code': 'VirtualMachineDoesNotExist',
                'message': 'Requested virtual machine instance was not found'
            }
        }), 404)


@vm.route('%s/%s' % (prefix, provider))
def list_vms_per_rg(subId, rgroup):
    """
    Lists all of the virtual machines in the specified resource group.
    Use the nextLink property in the response to get the next page of virtual machines.

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/list
    """
    # TODO: Add pagination(nextLink) support
    machines = VirtualMachine.objects.filter(
        subscription=subId, resourceGroup=rgroup).to_json()
    return jsonify(loads(machines))


@vm.route('<subId>/%s' % provider)
def list_vms_per_subscription(subId):
    """
    Lists all of the virtual machines in the specified subscription.
    Use the nextLink property in the response to get the next page of virtual machines.

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/listall
    """
    # TODO: Add pagination(nextLink) support
    machines = VirtualMachine.objects.filter(subscription=subId).to_json()
    return jsonify(loads(machines))
