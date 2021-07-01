
import mongoengine as db

from flask import current_app as app
from flask_mongoengine import MongoEngine


store = MongoEngine(app._get_current_object())


class ResourceGroup(db.Document):
    tags = db.DictField()
    name = db.StringField(required=True)
    managedBy = db.StringField(required=False)
    location = db.StringField(default='eastus')
    subscription = db.StringField(required=True)
    rid = db.StringField(required=True, unique=True)
    type = db.StringField(default='Microsoft.Resources/resourceGroups')
    properties = db.DictField(default={'provisioningState': 'Succeeded'})

    meta = {'collection': 'resourcegroups'}

    def __repr__(self):
        return "ResourceGroup(%s, %s)" % (self.name, self.subscription)

    def save(self, *args, **kwargs):
        self.managedBy = self.managedBy or self.subscription
        self.rid = '/subscriptions/%s/resourceGroups/%s' \
            % (self.subscription, self.name)
        super().save(args, kwargs)
