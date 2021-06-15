
import uuid
import mongoengine as db

from datetime import datetime
from flask import current_app as app
from flask_mongoengine import MongoEngine


class Properties:
    name = "example"
    subId = str(uuid.uuid4())
    tenant = str(uuid.uuid4())
    rgroup = "example-resource-group"


props = Properties()
store = MongoEngine(app._get_current_object())


class StorageAccount(db.Document):
    tags = db.DictField()
    name = db.StringField(required=True)
    location = db.StringField(required=True)
    kind = db.StringField(default='StorageV2')
    subscription = db.StringField(required=True)
    resourceGroup = db.StringField(required=True)
    rid = db.StringField(required=True, unique=True)
    tenant = db.StringField(required=True, default='test')
    type = db.StringField(default='Microsoft.Storage/storageAccounts')
    sku = db.DictField(default={'name': 'Standard_RAGRS', 'tier': 'Standard'})
    properties = db.DictField(default={
        "keyCreationTime": {
            "key1": datetime.isoformat(datetime.now()),
            "key2": datetime.isoformat(datetime.now())
        },
        "geoReplicationStats": {
            "status": "Live",
            "lastSyncTime": datetime.isoformat(datetime.now()),
            "canFailover": True
        },
        "isHnsEnabled": True,
        "creationTime": datetime.isoformat(datetime.now()),
        "networkAcls": {
            "bypass": "AzureServices",
            "defaultAction": "Allow",
            "ipRules": [],
            "virtualNetworkRules": [],
            "resourceAccessRules": [
                {
                    "tenantId": props.tenant,
                    "resourceId": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Synapse/workspaces/testworkspace"
                }
            ]
        },
        "primaryEndpoints": {
            "web": f"https://{props.name}.web.core.windows.net/",
            "dfs": f"https://{props.name}.dfs.core.windows.net/",
            "blob": f"https://{props.name}.blob.core.windows.net/",
            "file": f"https://{props.name}.file.core.windows.net/",
            "queue": f"https://{props.name}.queue.core.windows.net/",
            "table": f"https://{props.name}.table.core.windows.net/",
            "microsoftEndpoints": {
                "web": f"https://{props.name}-microsoftrouting.web.core.windows.net/",
                "dfs": f"https://{props.name}-microsoftrouting.dfs.core.windows.net/",
                "blob": f"https://{props.name}-microsoftrouting.blob.core.windows.net/",
                "file": f"https://{props.name}-microsoftrouting.file.core.windows.net/",
                "queue": f"https://{props.name}-microsoftrouting.queue.core.windows.net/",
                "table": f"https://{props.name}-microsoftrouting.table.core.windows.net/"
            },
            "internetEndpoints": {
                "web": f"https://{props.name}-internetrouting.web.core.windows.net/",
                "dfs": f"https://{props.name}-internetrouting.dfs.core.windows.net/",
                "blob": f"https://{props.name}-internetrouting.blob.core.windows.net/",
                "file": f"https://{props.name}-internetrouting.file.core.windows.net/"
            }
        },
        "primaryLocation": "eastus2",
        "provisioningState": "Succeeded",
        "routingPreference": {
            "routingChoice": "MicrosoftRouting",
            "publishMicrosoftEndpoints": True,
            "publishInternetEndpoints": True
        },
        "encryption": {
            "services": {
                "file": {
                    "keyType": "Account",
                    "enabled": True,
                    "lastEnabledTime": datetime.isoformat(datetime.now())
                },
                "blob": {
                    "keyType": "Account",
                    "enabled": True,
                    "lastEnabledTime": datetime.isoformat(datetime.now())
                }
            },
            "keySource": "Microsoft.Storage"
        },
        "secondaryLocation": "northcentralus(stage)",
        "statusOfPrimary": "available",
        "statusOfSecondary": "available",
        "supportsHttpsTrafficOnly": False
    })

    meta = {'collection': 'storageaccounts'}

    def __repr__(self):
        return "StorageAccount(%s)" % self.rid

    def save(self, *args, **kwargs):
        self.rid = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s' % (
            self.subscription, self.resourceGroup, self.type, self.name)
        super().save(args, kwargs)
