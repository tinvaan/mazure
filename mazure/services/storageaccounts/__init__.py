
from json import dumps
from gzip import compress
from flask import current_app as app
from flask_mongoengine import MongoEngine

from mazure.proxy import AzureInterceptor


store = MongoEngine(app._get_current_object())


class Responses:
    def openid(self):
        """Return the Open ID configuration"""
    openid.response = dict()
    openid.response.update({'status': 200})
    openid.response.update({
        'headers': {'Cache-Control': 'max-age=86400, private', 'Content-Type': 'application/json; charset=utf-8', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'X-Content-Type-Options': 'nosniff', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, OPTIONS', 'P3P': 'CP="DSP CUR OTPi IND OTRi ONL FIN"', 'x-ms-request-id': 'a717441c-4336-4e09-9a6f-ce5469c38100', 'x-ms-ests-server': '2.1.11722.21 - SCUS ProdSlices', 'Set-Cookie': 'fpc=AiiA5-ysrShKkmKWa1uOzi0; expires=Sun, 13-Jun-2021 11:29:53 GMT; path=/; secure; HttpOnly; SameSite=None, esctx=AQABAAAAAAD--DLA3VO7QrddgJg7WevrRBqddpxHlzKM1RcLCthcF2Hu4oTxfg-1lHjAuFsLmDKqUj96-aMic9xbHodfBlswg7fKcNnMprlqmFF5dAOWsEYD0j8Ag2F2i1F1fxdX0hRlOytVu5Um2UFoHYszN73-NsSvIOpWEkFN9oB5mTFaFLZvEsCPW9j6AtxRgAGS-UQgAA; domain=.login.microsoftonline.com; path=/; secure; HttpOnly; SameSite=None, x-ms-gateway-slice=estsfd; path=/; secure; samesite=none; httponly, stsservicecookie=estsfd; path=/; secure; samesite=none; httponly', 'Date': 'Fri, 14 May 2021 11:29:53 GMT', 'Content-Length': '1651'}
    })
    openid.response.update({
        'body': {'token_endpoint': 'https://login.microsoftonline.com/2193f4ca-f7b7-4a1b-8449-b76d1873d8e7/oauth2/v2.0/token', 'token_endpoint_auth_methods_supported': ['client_secret_post', 'private_key_jwt', 'client_secret_basic'], 'jwks_uri': 'https://login.microsoftonline.com/2193f4ca-f7b7-4a1b-8449-b76d1873d8e7/discovery/v2.0/keys', 'response_modes_supported': ['query', 'fragment', 'form_post'], 'subject_types_supported': ['pairwise'], 'id_token_signing_alg_values_supported': ['RS256'], 'response_types_supported': ['code', 'id_token', 'code id_token', 'id_token token'], 'scopes_supported': ['openid', 'profile', 'email', 'offline_access'], 'issuer': 'https://login.microsoftonline.com/2193f4ca-f7b7-4a1b-8449-b76d1873d8e7/v2.0', 'request_uri_parameter_supported': False, 'userinfo_endpoint': 'https://graph.microsoft.com/oidc/userinfo', 'authorization_endpoint': 'https://login.microsoftonline.com/2193f4ca-f7b7-4a1b-8449-b76d1873d8e7/oauth2/v2.0/authorize', 'device_authorization_endpoint': 'https://login.microsoftonline.com/2193f4ca-f7b7-4a1b-8449-b76d1873d8e7/oauth2/v2.0/devicecode', 'http_logout_supported': True, 'frontchannel_logout_supported': True, 'end_session_endpoint': 'https://login.microsoftonline.com/2193f4ca-f7b7-4a1b-8449-b76d1873d8e7/oauth2/v2.0/logout', 'claims_supported': ['sub', 'iss', 'cloud_instance_name', 'cloud_instance_host_name', 'cloud_graph_host_name', 'msgraph_host', 'aud', 'exp', 'iat', 'auth_time', 'acr', 'nonce', 'preferred_username', 'name', 'tid', 'ver', 'at_hash', 'c_hash', 'email'], 'tenant_region_scope': 'NA', 'cloud_instance_name': 'microsoftonline.com', 'cloud_graph_host_name': 'graph.windows.net', 'msgraph_host': 'graph.microsoft.com', 'rbac_url': 'https://pas.windows.net'}
    })

    def authorize(self):
        """Authorize against the Open ID response"""
    authorize.response = dict()
    authorize.response.update({'status': 200})
    authorize.response.update({
        'headers': {'Cache-Control': 'max-age=86400, private', 'Content-Length': '945', 'Content-Type': 'application/json; charset=utf-8', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'X-Content-Type-Options': 'nosniff', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, OPTIONS', 'P3P': 'CP="DSP CUR OTPi IND OTRi ONL FIN"', 'x-ms-request-id': '96bcad97-709f-4533-9955-cb1292f5cb00', 'x-ms-ests-server': '2.1.11654.25 - SEASLR1 ProdSlices', 'Set-Cookie': 'fpc=Ah_8TmrSCnxIjDFXS_AO6_8; expires=Sun, 13-Jun-2021 11:33:57 GMT; path=/; secure; HttpOnly; SameSite=None, esctx=AQABAAAAAAD--DLA3VO7QrddgJg7WevrXgefkMHUzYar92QtP00ImyqYE7vBNWonyIsVDFlrdKkcj1Y_uqMFRuoX9L9TuEWsbMX8Mq4xZ_M7DfQ1IIgyqmhJaiqwBMJJuerye4Sy6-BVLh2DlsviJQX18s_kvrA6wtYQ_PsaBsV-tNBecQnaN7CyCKFbtxaKO_16mQl6w5QgAA; domain=.login.microsoftonline.com; path=/; secure; HttpOnly; SameSite=None, x-ms-gateway-slice=estsfd; path=/; secure; samesite=none; httponly, stsservicecookie=estsfd; path=/; secure; samesite=none; httponly', 'Date': 'Fri, 14 May 2021 11:33:56 GMT'}
    })
    authorize.response.update({
        'body': {'tenant_discovery_endpoint': 'https://login.microsoftonline.com/common/.well-known/openid-configuration', 'api-version': '1.1', 'metadata': [{'preferred_network': 'login.microsoftonline.com', 'preferred_cache': 'login.windows.net', 'aliases': ['login.microsoftonline.com', 'login.windows.net', 'login.microsoft.com', 'sts.windows.net']}, {'preferred_network': 'login.partner.microsoftonline.cn', 'preferred_cache': 'login.partner.microsoftonline.cn', 'aliases': ['login.partner.microsoftonline.cn', 'login.chinacloudapi.cn']}, {'preferred_network': 'login.microsoftonline.de', 'preferred_cache': 'login.microsoftonline.de', 'aliases': ['login.microsoftonline.de']}, {'preferred_network': 'login.microsoftonline.us', 'preferred_cache': 'login.microsoftonline.us', 'aliases': ['login.microsoftonline.us', 'login.usgovcloudapi.net']}, {'preferred_network': 'login-us.microsoftonline.com', 'preferred_cache': 'login-us.microsoftonline.com', 'aliases': ['login-us.microsoftonline.com']}]}
    })

    def oauth(self):
        """OAuth authentication"""
    oauth.response = dict()
    oauth.response.update({'status': 200})
    oauth.response.update({
        'headers': {'Cache-Control': 'no-store, no-cache', 'Pragma': 'no-cache', 'Content-Type': 'application/json; charset=utf-8', 'Expires': '-1', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'X-Content-Type-Options': 'nosniff', 'P3P': 'CP="DSP CUR OTPi IND OTRi ONL FIN"', 'client-request-id': '8e5a26c3-7e76-4c6d-a7ea-86771458c527', 'x-ms-request-id': 'fb47697c-530f-4808-bfad-991a84adb500', 'x-ms-ests-server': '2.1.11722.21 - WUS2 ProdSlices', 'x-ms-clitelem': '1,0,0,,', 'Set-Cookie': 'fpc=AguNVSI_WW9GoGUULTe7QM2Psu5nAQAAAB9YMNgOAAAA; expires=Sun, 13-Jun-2021 11:38:07 GMT; path=/; secure; HttpOnly; SameSite=None, x-ms-gateway-slice=estsfd; path=/; secure; samesite=none; httponly, stsservicecookie=estsfd; path=/; secure; samesite=none; httponly', 'Date': 'Fri, 14 May 2021 11:38:06 GMT', 'Content-Length': '1349'}
    })
    oauth.response.update({
        'body': {'token_type': 'Bearer', 'expires_in': 3599, 'ext_expires_in': 3599, 'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuYXp1cmUuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMjE5M2Y0Y2EtZjdiNy00YTFiLTg0NDktYjc2ZDE4NzNkOGU3LyIsImlhdCI6MTYyMDk5MTk4NywibmJmIjoxNjIwOTkxOTg3LCJleHAiOjE2MjA5OTU4ODcsImFpbyI6IkUyWmdZRGpPSHlIS2J2TG5iVTNxdlVjeU9TKzNBQUE9IiwiYXBwaWQiOiIzODQ2N2MwYi0yMGIzLTRlZWItYmNhOS03YjJhMmViZDE2ZTQiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yMTkzZjRjYS1mN2I3LTRhMWItODQ0OS1iNzZkMTg3M2Q4ZTcvIiwib2lkIjoiYWEzYzZmNGItYTBlMC00MDY3LTk3ZTktZDQ0ZGJlMDE2ZDkwIiwicmgiOiIwLkFWa0F5dlNUSWJmM0cwcUVTYmR0R0hQWTV3dDhSaml6SU90T3ZLbDdLaTY5RnVSWkFBQS4iLCJzdWIiOiJhYTNjNmY0Yi1hMGUwLTQwNjctOTdlOS1kNDRkYmUwMTZkOTAiLCJ0aWQiOiIyMTkzZjRjYS1mN2I3LTRhMWItODQ0OS1iNzZkMTg3M2Q4ZTciLCJ1dGkiOiJmR2xILXc5VENFaV9yWmthaEsyMUFBIiwidmVyIjoiMS4wIiwieG1zX3RjZHQiOjE1OTU2MjQxODB9.KRg98aL6s1ohBmzfXVVCdBxQCCCkcy6YOSS5eQcQW2U-meyWv79kK6tgiNXJ6SLRAteiGaHMIX8d84VcDmVpiYL3-kQabvBqE8bgJZHgF3wpquHVX3veEQP0J-sQXTk5TFTNYlPax4kdCzX47dUcwsADxa7GUFiuU_mA6RCVoHeP-yUSvPlb6rjzG0Eqy4CJPisf7Z8f6dxK5B2oE8eWPjOtJuofL5ru_bIMVk1qOAzVNweiBvoT2EPQHCnYxRpFm8SUHaU3y36S8rSm4OOAxrQWX5TwRS69YCWvbeNLzlvQHZL4Ur0TP0RVVWmAaZvTIXtt1ZnYlgkYNid_lvq6tA'}
    })

    def list(self):
        """List storage accounts in a subscription"""
    list.response = dict()
    list.response.update({'status': 200})
    list.response.update({
        'headers': {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Content-Type': 'application/json; charset=utf-8', 'Content-Encoding': 'gzip', 'Expires': '-1', 'Vary': 'Accept-Encoding', 'x-ms-original-request-ids': '1b751f81-3452-401d-ad9d-41ee185c23e9, 162218ed-e5a2-442a-abab-36850e854e8d, 8622da85-a772-4274-9305-3f8cd9c29d39', 'x-ms-ratelimit-remaining-subscription-reads': '11909', 'x-ms-request-id': '16807962-d1e9-4d15-93ac-f1327818efbb', 'x-ms-correlation-request-id': '16807962-d1e9-4d15-93ac-f1327818efbb', 'x-ms-routing-request-id': 'SOUTHINDIA:20210514T181020Z:16807962-d1e9-4d15-93ac-f1327818efbb', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'X-Content-Type-Options': 'nosniff', 'Date': 'Fri, 14 May 2021 18:10:20 GMT', 'Content-Length': '1669'}
    })
    list.response.update({
        'body': {'value': [{'sku': {'name': 'Standard_RAGRS', 'tier': 'Standard'}, 'kind': 'StorageV2', 'id': '/subscriptions/24d61f39-b4be-4ada-a91d-0d6b451477c8/resourceGroups/vaibhav/providers/Microsoft.Storage/storageAccounts/vaibhavsa', 'name': 'vaibhavsa', 'type': 'Microsoft.Storage/storageAccounts', 'location': 'eastus', 'tags': {}, 'properties': {'privateEndpointConnections': [], 'minimumTlsVersion': 'TLS1_2', 'allowBlobPublicAccess': True, 'networkAcls': {'bypass': 'AzureServices', 'virtualNetworkRules': [], 'ipRules': [], 'defaultAction': 'Allow'}, 'supportsHttpsTrafficOnly': True, 'encryption': {'services': {'file': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2020-10-20T08:12:10.6103426Z'}, 'blob': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2020-10-20T08:12:10.6103426Z'}}, 'keySource': 'Microsoft.Storage'}, 'accessTier': 'Hot', 'provisioningState': 'Succeeded', 'creationTime': '2020-10-20T08:12:10.5166061Z', 'primaryEndpoints': {'dfs': 'https://vaibhavsa.dfs.core.windows.net/', 'web': 'https://vaibhavsa.z13.web.core.windows.net/', 'blob': 'https://vaibhavsa.blob.core.windows.net/', 'queue': 'https://vaibhavsa.queue.core.windows.net/', 'table': 'https://vaibhavsa.table.core.windows.net/', 'file': 'https://vaibhavsa.file.core.windows.net/'}, 'primaryLocation': 'eastus', 'statusOfPrimary': 'available', 'secondaryLocation': 'westus', 'statusOfSecondary': 'available', 'secondaryEndpoints': {'dfs': 'https://vaibhavsa-secondary.dfs.core.windows.net/', 'web': 'https://vaibhavsa-secondary.z13.web.core.windows.net/', 'blob': 'https://vaibhavsa-secondary.blob.core.windows.net/', 'queue': 'https://vaibhavsa-secondary.queue.core.windows.net/', 'table': 'https://vaibhavsa-secondary.table.core.windows.net/'}}}, {'sku': {'name': 'Standard_RAGRS', 'tier': 'Standard'}, 'kind': 'BlobStorage', 'id': '/subscriptions/24d61f39-b4be-4ada-a91d-0d6b451477c8/resourceGroups/vgs-rg/providers/Microsoft.Storage/storageAccounts/vgssca', 'name': 'vgssca', 'type': 'Microsoft.Storage/storageAccounts', 'location': 'eastus', 'tags': {}, 'properties': {'privateEndpointConnections': [], 'routingPreference': {'routingChoice': 'InternetRouting', 'publishMicrosoftEndpoints': False, 'publishInternetEndpoints': False}, 'minimumTlsVersion': 'TLS1_2', 'allowBlobPublicAccess': True, 'allowSharedKeyAccess': False, 'networkAcls': {'bypass': 'AzureServices', 'virtualNetworkRules': [], 'ipRules': [], 'defaultAction': 'Allow'}, 'supportsHttpsTrafficOnly': False, 'encryption': {'services': {'file': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2021-04-12T07:19:01.1342075Z'}, 'blob': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2021-04-12T07:19:01.1342075Z'}}, 'keySource': 'Microsoft.Storage'}, 'accessTier': 'Hot', 'provisioningState': 'Succeeded', 'creationTime': '2021-04-12T07:19:01.0404445Z', 'primaryEndpoints': {'dfs': 'https://vgssca.dfs.core.windows.net/', 'blob': 'https://vgssca.blob.core.windows.net/', 'table': 'https://vgssca.table.core.windows.net/'}, 'primaryLocation': 'eastus', 'statusOfPrimary': 'available', 'secondaryLocation': 'westus', 'statusOfSecondary': 'available', 'secondaryEndpoints': {'dfs': 'https://vgssca-secondary.dfs.core.windows.net/', 'blob': 'https://vgssca-secondary.blob.core.windows.net/', 'table': 'https://vgssca-secondary.table.core.windows.net/'}}}, {'sku': {'name': 'Standard_LRS', 'tier': 'Standard'}, 'kind': 'Storage', 'id': '/subscriptions/24d61f39-b4be-4ada-a91d-0d6b451477c8/resourceGroups/test-fn/providers/Microsoft.Storage/storageAccounts/storageaccounttestfb9b8', 'name': 'storageaccounttestfb9b8', 'type': 'Microsoft.Storage/storageAccounts', 'location': 'centralus', 'tags': {}, 'properties': {'privateEndpointConnections': [], 'networkAcls': {'bypass': 'AzureServices', 'virtualNetworkRules': [], 'ipRules': [], 'defaultAction': 'Allow'}, 'supportsHttpsTrafficOnly': True, 'encryption': {'services': {'file': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2020-09-24T09:59:54.7704566Z'}, 'blob': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2020-09-24T09:59:54.7704566Z'}}, 'keySource': 'Microsoft.Storage'}, 'provisioningState': 'Succeeded', 'creationTime': '2020-09-24T09:59:54.6767211Z', 'primaryEndpoints': {'blob': 'https://storageaccounttestfb9b8.blob.core.windows.net/', 'queue': 'https://storageaccounttestfb9b8.queue.core.windows.net/', 'table': 'https://storageaccounttestfb9b8.table.core.windows.net/', 'file': 'https://storageaccounttestfb9b8.file.core.windows.net/'}, 'primaryLocation': 'centralus', 'statusOfPrimary': 'available'}}, {'sku': {'name': 'Standard_RAGRS', 'tier': 'Standard'}, 'kind': 'StorageV2', 'id': '/subscriptions/24d61f39-b4be-4ada-a91d-0d6b451477c8/resourceGroups/rampup/providers/Microsoft.Storage/storageAccounts/rampupdeleteme', 'name': 'rampupdeleteme', 'type': 'Microsoft.Storage/storageAccounts', 'location': 'centralindia', 'tags': {}, 'properties': {'privateEndpointConnections': [], 'minimumTlsVersion': 'TLS1_2', 'allowBlobPublicAccess': True, 'allowSharedKeyAccess': True, 'networkAcls': {'bypass': 'AzureServices', 'virtualNetworkRules': [], 'ipRules': [], 'defaultAction': 'Allow'}, 'supportsHttpsTrafficOnly': True, 'encryption': {'services': {'file': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2021-02-12T15:38:16.2187791Z'}, 'blob': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2021-02-12T15:38:16.2187791Z'}}, 'keySource': 'Microsoft.Storage'}, 'accessTier': 'Hot', 'provisioningState': 'Succeeded', 'creationTime': '2021-02-12T15:38:16.1562771Z', 'primaryEndpoints': {'dfs': 'https://rampupdeleteme.dfs.core.windows.net/', 'web': 'https://rampupdeleteme.z29.web.core.windows.net/', 'blob': 'https://rampupdeleteme.blob.core.windows.net/', 'queue': 'https://rampupdeleteme.queue.core.windows.net/', 'table': 'https://rampupdeleteme.table.core.windows.net/', 'file': 'https://rampupdeleteme.file.core.windows.net/'}, 'primaryLocation': 'centralindia', 'statusOfPrimary': 'available', 'secondaryLocation': 'southindia', 'statusOfSecondary': 'available', 'secondaryEndpoints': {'dfs': 'https://rampupdeleteme-secondary.dfs.core.windows.net/', 'web': 'https://rampupdeleteme-secondary.z29.web.core.windows.net/', 'blob': 'https://rampupdeleteme-secondary.blob.core.windows.net/', 'queue': 'https://rampupdeleteme-secondary.queue.core.windows.net/', 'table': 'https://rampupdeleteme-secondary.table.core.windows.net/'}}}, {'sku': {'name': 'Standard_RAGRS', 'tier': 'Standard'}, 'kind': 'StorageV2', 'id': '/subscriptions/24d61f39-b4be-4ada-a91d-0d6b451477c8/resourceGroups/rampup/providers/Microsoft.Storage/storageAccounts/rampupsa', 'name': 'rampupsa', 'type': 'Microsoft.Storage/storageAccounts', 'location': 'centralindia', 'tags': {'Name': 'rampup-sa', 'Exercise': 'Rampup', 'Testing': 'True'}, 'properties': {'privateEndpointConnections': [], 'minimumTlsVersion': 'TLS1_2', 'allowBlobPublicAccess': True, 'networkAcls': {'bypass': 'AzureServices', 'virtualNetworkRules': [], 'ipRules': [], 'defaultAction': 'Allow'}, 'supportsHttpsTrafficOnly': True, 'encryption': {'services': {'file': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2021-01-04T10:29:02.4877863Z'}, 'blob': {'keyType': 'Account', 'enabled': True, 'lastEnabledTime': '2021-01-04T10:29:02.4877863Z'}}, 'keySource': 'Microsoft.Storage'}, 'accessTier': 'Hot', 'provisioningState': 'Succeeded', 'creationTime': '2021-01-04T10:29:02.4253018Z', 'primaryEndpoints': {'dfs': 'https://rampupsa.dfs.core.windows.net/', 'web': 'https://rampupsa.z29.web.core.windows.net/', 'blob': 'https://rampupsa.blob.core.windows.net/', 'queue': 'https://rampupsa.queue.core.windows.net/', 'table': 'https://rampupsa.table.core.windows.net/', 'file': 'https://rampupsa.file.core.windows.net/'}, 'primaryLocation': 'centralindia', 'statusOfPrimary': 'available', 'secondaryLocation': 'southindia', 'statusOfSecondary': 'available', 'secondaryEndpoints': {'dfs': 'https://rampupsa-secondary.dfs.core.windows.net/', 'web': 'https://rampupsa-secondary.z29.web.core.windows.net/', 'blob': 'https://rampupsa-secondary.blob.core.windows.net/', 'queue': 'https://rampupsa-secondary.queue.core.windows.net/', 'table': 'https://rampupsa-secondary.table.core.windows.net/'}}}]}
    })

    def check(self):
        """Check if a requested storage account name is available"""
    check.response = dict()
    check.response.update({'status': 200})
    check.response.update({
        'headers': {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Transfer-Encoding': 'chunked', 'Content-Type': 'application/json', 'Content-Encoding': 'gzip', 'Expires': '-1', 'Vary': 'Accept-Encoding', 'x-ms-request-id': '7fb7fa36-6656-4cb6-a100-caf9f5dd5c82', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Server': 'Microsoft-Azure-Storage-Resource-Provider/1.0,Microsoft-HTTPAPI/2.0 Microsoft-HTTPAPI/2.0', 'x-ms-ratelimit-remaining-subscription-reads': '11690', 'x-ms-correlation-request-id': '56442e0f-e7ca-4636-a58e-d0809c33aa16', 'x-ms-routing-request-id': 'SOUTHINDIA:20210514T192716Z:56442e0f-e7ca-4636-a58e-d0809c33aa16', 'X-Content-Type-Options': 'nosniff', 'Date': 'Fri, 14 May 2021 19:27:15 GMT'}
    })
    check.response.update({
        'body': {'nameAvailable': True}
    })


class StorageAccountProxy(AzureInterceptor):
    def callback(self, request):
        response = Responses()
        if ".well-known/openid-configuration" in request.path_url:
            return (
                response.openid.response.get('status'),
                response.openid.response.get('headers'),
                dumps(response.openid.response.get('body'))
            )

        if ("common/oauth2/authorize" in request.path_url and
                "common/discovery/instance" in request.path_url):
            return (
                response.authorize.response.get('status'),
                response.authorize.response.get('headers'),
                dumps(response.authorize.response.get('body'))
            )

        if "oauth2/v2.0/token" in request.path_url:
            return (
                response.oauth.response.get('status'),
                response.oauth.response.get('headers'),
                dumps(response.oauth.response.get('body'))
            )

        if "checkNameAvailability" in request.path_url:
            return (
                response.check.response.get('status'),
                response.check.response.get('headers'),
                compress(
                    bytes(dumps(response.check.response.get('body')), 'utf-8'))
            )

        if "storageAccounts?" in request.path_url:
            return (
                response.list.response.get('status'),
                response.list.response.get('headers'),
                compress(
                    bytes(dumps(response.list.response.get('body')), 'utf-8')
                )
            )
