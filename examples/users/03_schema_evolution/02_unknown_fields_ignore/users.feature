Feature: User focused example

  Scenario: Demonstrate Unknown Fields Ignore
    Given the example table:
      | username | team     |
      | alice    | Platform |
    Then the unknown fields ignore behavior is correct

