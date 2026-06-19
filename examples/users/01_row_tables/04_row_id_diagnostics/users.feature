Feature: User focused example

  Scenario: Demonstrate Row ID Diagnostics
    Given the example table:
      | status  | user id |
      | blocked | U-500   |
    Then the row id diagnostics behavior is correct

