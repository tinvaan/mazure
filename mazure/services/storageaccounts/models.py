
import mongoengine as db

from datetime import datetime
from flask import current_app as app
from flask_mongoengine import MongoEngine


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
        "networkAcls": {
            "bypass": "AzureServices",
            "virtualNetworkRules": [],
            "ipRules": [],
            "defaultAction": "Allow"
        },
        "supportsHttpsTrafficOnly": True,
        "encryption": {
            "services": {
                "file": {
                    "enabled": True,
                    "lastEnabledTime": datetime.isoformat(datetime.now())
                },
                "blob": {
                    "enabled": True,
                    "lastEnabledTime": datetime.isoformat(datetime.now())
                }
            },
            "keySource": "Microsoft.Storage"
        },
        "accessTier": "Hot",
        "provisioningState": "Succeeded",
        "creationTime": datetime.isoformat(datetime.now()),
        "primaryEndpoints": {
            "blob": "https://rampupsa.blob.core.windows.net/",
            "queue": "https://rampupsa.queue.core.windows.net/",
            "table": "https://rampupsa.table.core.windows.net/",
            "file": "https://rampupsa.file.core.windows.net/"
        },
        "primaryLocation": "centralindia",
        "statusOfPrimary": "available",
        "secondaryLocation": "southindia",
        "statusOfSecondary": "available",
        "secondaryEndpoints": {
            "blob": "https://rampupsa-secondary.blob.core.windows.net/",
            "queue": "https://rampupsa-secondary.queue.core.windows.net/",
            "table": "https://rampupsa-secondary.table.core.windows.net/"
        }
    })

    meta = {'collection': 'storageaccounts'}

    def __repr__(self):
        return "StorageAccount(%s)" % self.rid

    def save(self, *args, **kwargs):
        self.rid = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s' % (
            self.subscription, self.resourceGroup, self.type, self.name)
        super().save(args, kwargs)
