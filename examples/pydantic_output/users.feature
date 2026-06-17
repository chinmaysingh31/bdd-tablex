Feature: Pydantic output models

  Scenario: Validate and return Pydantic users
    Given the following Pydantic users exist:
      | name  | age |
      | Alice | 30  |
    Then the user is a validated Pydantic model
