
Feature: Azure virtual machine methods

    Scenario: Query virtual machines in an inactive subscription
        Given Virtual machines are not present in a subscription
        And Virtual machines are queried in the subscription
        Then Return an empty list of virtual machines

    Scenario: Query virtual machines in an active subscription
        Given Virtual machines are present in a subscription
        And Virtual machines are queried in the subscription
        Then Return a list of existing virtual machines

    Scenario: Query virtual machines in an inactive resource group
        Given Virtual machines are not present in a resource group
        And Virtual machines are queried in the resource group
        Then Return an empty list of virtual machines

    Scenario: Query virtual machines in an active resource group
        Given Virtual machines are present in a resource group
        And Virtual machines are queried in the resource group
        Then Return a list of existing virtual machines

    Scenario: Query a non-existent virtual machine in a resource group
        Given Virtual machines are present in a resource group
        And Virtual machine with name "foobar" is queried
        Then Raise a ResourceNotFoundError

    Scenario: Query an existing virtual machine in a resource group
        Given Virtual machines are present in a resource group
        And Virtual machine with name "first-vm" is queried
        Then Return information for virtual machine with name "first-vm"

    Scenario: Create a virtual machine in a resource group
        Given Virtual machines are present in a resource group
        And New virtual machine with name "new-vm" is created
        When Virtual machine with name "new-vm" is queried
        Then Return information for virtual machine with name "new-vm"

    Scenario: Create a virtual machine with invalid name in a resource group
        Given Virtual machines are present in a resource group
            And New virtual machine with name "new-vm" is created
        When New virtual machine with name "new-vm" is created
        Then Raise an exception

    Scenario: Delete an existing virtual machine
        Given Virtual machines are present in a resource group
            And Virtual machine with name "first-vm" is deleted
        When Virtual machine with name "first-vm" is queried
        Then Raise an exception

    Scenario: Delete a non-existent virtual machine
        Given Virtual machines are not present in a resource group
        And Virtual machine with name "first-vm" is deleted
        Then Virtual machine is silently deleted

    Scenario: Create and delete a virtual machine
        Given Virtual machines are present in a resource group
            And New virtual machine with name "new-vm" is created
            When Virtual machine with name "new-vm" is queried
            Then Return information for virtual machine with name "new-vm"
        And Virtual machine with name "new-vm" is deleted
            When Virtual machine with name "new-vm" is queried
            Then Raise an exception
