
Feature: Azure storage account methods

    Scenario: Request storage account creation with new account name
        Given Storage accounts are setup
        And New storage account name is requested
        Then Return truthy availability

    Scenario: Request storage account creation with existing account name
        Given Storage accounts are setup
        And Existing storage account name is requested
        Then Return falsy availability

    Scenario: Query storage accounts for a new subscription
        Given Storage accounts are not setup
        And Storage accounts are queried
        Then Return an empty list of storage accounts

    Scenario: Query storage accounts for an existing subscription
        Given Storage accounts are setup
        And Storage accounts are queried
        Then Return a list of existing storage accounts
