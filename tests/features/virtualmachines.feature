
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
        Then Return information for a virtual machine with name "first-vm"
