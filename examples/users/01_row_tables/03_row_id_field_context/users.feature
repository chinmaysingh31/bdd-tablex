Feature: User focused example

  Scenario: Demonstrate Row ID Field Context
    Given the example table:
      | display name | user id |
      | Alice        | U-100   |
    Then the row id field context behavior is correct

