Feature: Whole-table validation

  Scenario: Validate relationships across several users
    Given the following team users exist:
      | email             | primary |
      | owner@example.com | yes     |
      | editor@example.com| no      |
    Then the complete user table is valid
