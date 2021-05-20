
Feature: Azure storage account methods

    Scenario: Request storage account creation with new account name
        Given Storage accounts are setup
        And New storage account name is requested
        Then Storage account name is available

    Scenario: Request storage account creation with existing account name
        Given Storage accounts are setup
        And Existing storage account name is requested
        Then Storage account name is unavailable

    Scenario: Query storage accounts for a new subscription
        Given Storage accounts are not setup
        And Storage accounts are queried
        Then Return an empty list of storage accounts

    Scenario: Query storage accounts for an existing subscription
        Given Storage accounts are setup
        And Storage accounts are queried
        Then Return a list of existing storage accounts

    Scenario: Create a new storage account with valid name
        Given Storage accounts are setup
            And New storage account name is requested
            And Storage account name is available
        When New storage account is created with name "fifth"
        Then Requested name is found in list of storage accounts

    Scenario: Create a new storage account with invalid name
        Given Storage accounts are setup
            And Existing storage account name is requested
            And Storage account name is unavailable
        When New storage account is created with name "third"
        Then Create operation raises an error

    Scenario: Delete an existing storage account
        Given Storage accounts are setup
        And Storage account with name "first" is deleted
        Then Deleted account is not found in list of storage accounts

    Scenario: Delete a non-existent storage account
        Given Storage accounts are setup
        And Storage account with name "tenth" is deleted
        Then List of storage accounts is unchanged
