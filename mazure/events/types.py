
class Authorization:
    def __init__(self, data):
        self.scope = data.get('scope') if data else ""
        self.action = data.get('action') if data else ""


class Claims:
    def __init__(self, data):
        """TODO"""


class LocalizedString:
    def __init__(self, data):
        self.value = data.get('value')
        self.localized_value = data.get('localizedValue')

    def __repr__(self):
        return "LocalizedString(%s, %s)" % (self.value, self.localized_value)


class EventProperty:
    def __init__(self, data):
        self.entity = data.get('entity')
        self.message = data.get('message')
        self.hierarchy = data.get('hierarchy')
        self.event_category = data.get('eventCategory')


class EventLog:
    """
    This class maps to Azure activity log's EventData class
    """
    def __init__(self, event):
        self.authorization = Authorization(event.get('authorization'))
        self.caller = event.get('caller')
        self.channel = event.get('channels')
        self.claims = Claims(event.get('claims'))
        self.correlation_id = event.get('correlationId')
        self.description = event.get('description')
        self.event_data_id = event.get('eventDataId')
        self.event_name = LocalizedString(event.get('eventName'))
        self.category = LocalizedString(event.get('category'))
        self.event_timestamp = event.get('eventTimestamp')
        self.id = event.get('id')
        self.level = event.get('level')
        self.operation_id = event.get('operationId')
        self.operation_name = LocalizedString(event.get('operationName'))
        self.resource_group_name = event.get('resourceGroupName')
        self.resource_provider_name = LocalizedString(event.get('resourceProviderName'))
        self.resource_type = LocalizedString(event.get('resourceType'))
        self.resource_id = event.get('resourceId')
        self.status = LocalizedString(event.get('status'))
        self.sub_status = LocalizedString(event.get('subStatus'))
        self.submission_timestamp = event.get('submissionTimestamp')
        self.subscription_id = event.get('subscriptionId')
        self.tenant_id = event.get('tenantId')
        self.related_events = event.get('relatedEvents')

    def __repr__(self):
        return "EventLog<%s>" % self.resource_id
