# Mazure - [Moto](https://github.com/spulec/moto) for Azure

A library that allows you to mock Azure services.

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


class TestVirtualMachines(unittest.TestCase):
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

## Azure Services

`Mazure` is still very much a work in progress and aims to eventually implement the basic functionality of some of the most commonly used Azure services. At present, `Mazure` is able to mock the <em><strong>basic</strong></em> functionality of the below mentioned services.
- Storage accounts
- Virtual machines


## Resources
- [Azure REST API sample responses](https://github.com/Azure/azure-rest-api-specs/tree/master/specification)
