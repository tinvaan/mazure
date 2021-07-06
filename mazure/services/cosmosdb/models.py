
import uuid
import mongoengine as db

from datetime import datetime
from flask import current_app as app
from flask_mongoengine import MongoEngine


class Properties:
    document = "ddb1"
    account = "account1"
    location = "eastus"
    subId = str(uuid.uuid4())
    rgroup = "default-resource-group"


props = Properties()
store = MongoEngine(app._get_current_object())


class Database(db.EmbeddedDocument):
    _self = db.StringField()
    _rid = db.StringField(required=True)
    _colls = db.StringField(default='colls\/')
    _users = db.StringField(default='users\/')
    _ts = db.DateTimeField(default=datetime.now())
    _etag = db.StringField(default=str(uuid.uuid5()))
    uid = db.StringField(required=True, unique=True)

    def save(self, *args, **kwargs):
        self._self = "dbs\/%s\/" % self._rid


class DatabaseAccount(db.Document):
    tags = db.DictField()
    name = db.StringField(required=True)
    location = db.StringField(required=True)
    subscription = db.StringField(required=True)
    resourceGroup = db.StringField(required=True)
    rid = db.StringField(required=True, unique=True)
    kind = db.StringField(default="GlobalDocumentDB")
    databases = db.ListField(db.EmbeddedDocumentField(Database))
    type = db.StringField(default="Microsoft.DocumentDB/databaseAccounts")
    systemData = db.DictField(default={
        'createdAt': datetime.isoformat(datetime.now())
    })
    properties = db.DictField(default={
        "provisioningState": "Succeeded",
        "documentEndpoint": f"https://{props.document}.documents.azure.com:443/",
        "ipRules": [],
        "isVirtualNetworkFilterEnabled": False,
        "virtualNetworkRules": [],
        "databaseAccountOfferType": "Standard",
        "disableKeyBasedMetadataWriteAccess": False,
        "consistencyPolicy": {
            "defaultConsistencyLevel": "Session",
            "maxIntervalInSeconds": 5,
            "maxStalenessPrefix": 100
        },
        "writeLocations": [
            {
                "id": f"{props.document}-{props.location}",
                "locationName": "East US",
                "documentEndpoint": f"https://{props.document}-{props.location}.documents.azure.com:443/",
                "provisioningState": "Succeeded",
                "failoverPriority": 0
            }
        ],
        "readLocations": [
            {
                "id": f"{props.document}-{props.location}",
                "locationName": "East US",
                "documentEndpoint": f"https://{props.document}-{props.location}.documents.azure.com:443/",
                "provisioningState": "Succeeded",
                "failoverPriority": 0
            }
        ],
        "locations": [
            {
                "id": f"{props.document}-{props.location}",
                "locationName": "East US",
                "documentEndpoint": f"https://{props.document}-{props.location}.documents.azure.com:443/",
                "provisioningState": "Succeeded",
                "failoverPriority": 0
            }
        ],
        "failoverPolicies": [
            {
                "id": f"{props.document}-{props.location}",
                "locationName": "East US",
                "failoverPriority": 0
            }
        ],
        "privateEndpointConnections": [
            {
                "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.DocumentDB/databaseAccounts/{props.account}/privateEndpointConnections/pe1",
                "properties": {
                    "privateEndpoint": {
                        "id": f"/subscriptions/{props.subId}/resourceGroups/{props.rgroup}/providers/Microsoft.Network/privateEndpoints/pe1"
                    },
                    "privateLinkServiceConnectionState": {
                        "status": "Approved",
                        "actionsRequired": "None"
                    }
                }
            }
        ],
        "cors": [],
        "enableFreeTier": False,
        "apiProperties": {},
        "enableAnalyticalStorage": True,
        "backupPolicy": {
            "type": "Periodic",
            "periodicModeProperties": {
                "backupIntervalInMinutes": 240,
                "backupRetentionIntervalInHours": 8
            }
        },
        "networkAclBypass": "None",
        "networkAclBypassResourceIds": []
    })

    meta = {'collection': 'cosmosdb'}

    def save(self, *args, **kwargs):
        self.rid = "/subscriptions/%s/resourceGroups/%s/providers/%s/%s" % (
            self.subscription, self.resourceGroup, self.type, self.name)
        super().save(args, kwargs)
