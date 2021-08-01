# Mazure - [Moto](https://github.com/spulec/moto) for Azure

[![Build Status](https://cloud.drone.io/api/badges/tinvaan/mazure/status.svg)](https://cloud.drone.io/tinvaan/mazure)

A library that allows you to mock Azure services.

[![Demo](screenshots/mazure-demo.jpg)](https://www.youtube.com/watch?v=WCLCNlima0M)


## Installation
```bash
$ pip install --editable .
```

## Usage
`Mazure` provides two modes of operation. It can be used as a <br/>
- Context Manager
- Function Decorator

<br/>

Imagine a test setup as follows. To this
```python
import uuid
import secrets
import unittest

from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters


class TestStorageAccounts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subscription = str(uuid.uuid4())
        cls.creds = ClientSecretCredential(
            tenant_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            client_secret=secrets.token_urlsafe())
        cls.client = StorageManagementClient(cls.creds, cls.subscription)

    def test_create_and_list(self):
        """ TODO
        Creates a storage account & lists all storage accounts in a subscription
        """
```


### Function Decorator
Simply wrap your test function with a `@mazure` decorator.

```python
...
...
from mazure import mazure   # Import the mazure decorator


class TestStorageAccounts(unittest.TestCase):
    ...
    ...

    @mazure
    def test_create_and_list(self):
        accounts = self.client.storage_accounts.list()
        self.assertEqual(len([account for account in accounts]), 0)

        kws = {
            "sku": {"name": "Premium_LRS"},
            "kind": "BlockBlobStorage",
            "location": "eastus",
        }
        self.client.storage_accounts.begin_create(
            'testrg', 'testaccount', StorageAccountCreateParameters(**kws))
        accounts = self.client.storage_accounts.list()
        self.assertGreater(len([account for account in accounts]), 0)
```

### Context Manager
Make use of the `Mazure` class to mock out calls to the Azure API's

```python
...
...

from mazure import Mazure   # Import the Mazure class


class TestStorageAccounts(unittest.TestCase):
    ...
    ...

    def test_create_and_list(self):
        with Mazure():
            accounts = self.client.storage_accounts.list()
            self.assertEqual(len([account for account in accounts]), 0)

            kws = {
                "sku": {"name": "Premium_LRS"},
                "kind": "BlockBlobStorage",
                "location": "eastus",
            }
            self.client.storage_accounts.begin_create(
                'testrg', 'testaccount', StorageAccountCreateParameters(**kws))
            accounts = self.client.storage_accounts.list()
            self.assertGreater(len([account for account in accounts]), 0)
```

## Usage options
With both the decorator and the context manager, Mazure allows you some fine tuning options.

- ### Selective mocking
    You can request only certain services to be mocked in your code. For instance,
    ```python
    @mazure('storage_accounts', 'blob_services')
    def method(self):
        storage = StorageManagementClient(self.creds, self.subscription)
        compute = ComputeManagementClient(self.creds, self.subscription)
        accounts = [acc for acc in storage.storage_accounts.list()]
        machines = [vm for vm in compute.virtual_machines.list_all()]
        return accounts, machines
    ```
    In the above code block, only storage account API calls are mocked out. API calls to any other Azure services will raise an exception.

    When using a context manager, provide a list of services to be mocked
    ```python
    def method(self):
        with Mazure(['storage_accounts', 'blob_services']):
            ...
            ...
    ```
- ### Passthrough option
    To avoid the above scenario, you can use the `allow=True` flag in your decorator, which allows all unmocked API calls to pass through to query the live Azure API's.
    ```python
    @mazure('storage_accounts', 'blob_services', allow=True)
    def method(self):
        ...
        ...
    ```
    When using a context manager, the same functionality is available as follows.
    ```python
    def method(self):
        with Mazure(['storage_accounts', 'blob_services'], allow=True):
            ...
            ...
    ```

## Supported Azure Services

`Mazure` is still very much a work in progress and aims to eventually implement the basic functionality of some of the most commonly used Azure services. At present, `Mazure` is able to mock the <em><strong>basic</strong></em> functionality of the below mentioned services.
- Resource groups
- Storage accounts
- Virtual machines


## Resources
- [Azure REST API sample responses](https://github.com/Azure/azure-rest-api-specs/tree/master/specification)
