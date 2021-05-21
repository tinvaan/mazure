
import uuid
import mongoengine as db

from flask import current_app as app
from flask_mongoengine import MongoEngine


class Properties:
    name = "example"
    nic = "example-nic"
    disk = "example-disk"
    vmId = str(uuid.uuid4())
    subId = str(uuid.uuid4())
    rgroup = "example-resource-group"
    availabilitySet = "example-availability-set"
    ppg = "example-proximity-placement-group"


props = Properties()
store = MongoEngine(app._get_current_object())


class VirtualMachine(db.Document):
    tags = db.DictField()
    name = db.StringField(required=True)
    location = db.StringField(required=True)
    subscription = db.StringField(required=True)
    resourceGroup = db.StringField(required=True)
    rid = db.StringField(required=True, unique=True)
    provisioningState = db.StringField(default='Succeeded')
    type = db.StringField(default='Microsoft.Compute/virtualMachines')
    properties = db.DictField(default={
        "vmId": props.vmId,
        "availabilitySet": {
            "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Compute/availabilitySets/my-AvailabilitySet"
        },
        "proximityPlacementGroup": {
            "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Compute/proximityPlacementGroups/{props.ppg}"
        },
        "hardwareProfile": {
            "vmSize": "Standard_DS3_v2"
        },
        "storageProfile": {
            "imageReference": {
                "publisher": "MicrosoftWindowsServer",
                "offer": "WindowsServer",
                "sku": "2016-Datacenter",
                "version": "latest"
            },
            "osDisk": {
                "osType": "Windows",
                "name": "myOsDisk",
                "createOption": "FromImage",
                "caching": "ReadWrite",
                "managedDisk": {
                    "storageAccountType": "Premium_LRS",
                    "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Compute/disks/{props.disk}"
                },
                "diskSizeGB": 30
            },
            "dataDisks": [
                {
                    "lun": 0,
                    "name": "myDataDisk0",
                    "createOption": "Empty",
                    "caching": "ReadWrite",
                    "managedDisk": {
                        "storageAccountType": "Premium_LRS",
                        "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Compute/disks/{props.disk}"
                    },
                    "diskSizeGB": 30
                },
                {
                    "lun": 1,
                    "name": "myDataDisk1",
                    "createOption": "Attach",
                    "caching": "ReadWrite",
                    "managedDisk": {
                        "storageAccountType": "Premium_LRS",
                        "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Compute/disks/{props.disk}"
                    },
                    "diskSizeGB": 100
                }
            ]
        },
        "userData": "RXhhbXBsZSBVc2VyRGF0YQ==",
        "osProfile": {
            "computerName": "myVM",
            "adminUsername": "admin",
            "windowsConfiguration": {
                "provisionVMAgent": True,
                "enableAutomaticUpdates": False
            },
            "secrets": []
        },
        "networkProfile": {
            "networkInterfaces": [
                {
                    "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Network/networkInterfaces/{props.nic}"
                }
            ]
        },
        "diagnosticsProfile": {
            "bootDiagnostics": {
                "enabled": True,
                "storageUri": f"http://{props.name}.blob.core.windows.net"
            }
        },
        "extensionsTimeBudget": "PT50M",
        "provisioningState": "Succeeded"
    })

    meta = {'collection': 'resources'}

    def __repr__(self):
        return "VirtualMachine(%s)" % self.rid

    def save(self, *args, **kwargs):
        self.rid = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s' % (
            self.subscription, self.resourceGroup, self.type, self.name)
        super().save(args, kwargs)
