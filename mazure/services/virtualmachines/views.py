
from json import loads
from mongoengine.errors import ValidationError
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
    return jsonify({'value': loads(machines)})


@vm.route('<subId>/%s' % provider)
def list_vms_per_subscription(subId):
    """
    Lists all of the virtual machines in the specified subscription.
    Use the nextLink property in the response to get the next page of virtual machines.

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/listall
    """
    # TODO: Add pagination(nextLink) support
    machines = VirtualMachine.objects.filter(subscription=subId).to_json()
    return jsonify({'value': loads(machines)})


@vm.route('%s/%s/<vmName>' % (prefix, provider), methods=['PUT'])
def create_or_update(subId, rgroup, vmName):
    """
    The operation to create or update a virtual machine

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtual-machines/create-or-update
    """
    try:
        data = request.get_json(force=True)
        data.update({
            'name': vmName,
            'subscription': subId,
            'resourceGroup': rgroup,
            'provisioningState': 'Creating'
        })
        machine = VirtualMachine(**data)
        machine.save()
        return jsonify(loads(machine.to_json()))
    except ValidationError:
        return make_response(jsonify({
            'error': {
                'code': 'InvalidParameters',
                'message': 'Incorrect parameter values provided for create'
            }
        }), 400)


@vm.route('%s/%s/<vmName>' % (prefix, provider), methods=['DELETE'])
def delete_virtual_machine(subId, rgroup, vmName):
    """
    The operation to delete a virtual machine

    Ref: https://docs.microsoft.com/en-us/rest/api/compute/virtual-machines/delete
    """
    try:
        machine = VirtualMachine.objects.get(
            name=vmName, subscription=subId, resourceGroup=rgroup)
        machine.delete()
        return jsonify(loads(machine.to_json()))
    except VirtualMachine.DoesNotExist:
        return ('', 204)
