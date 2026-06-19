Feature: User focused example

  Scenario: Demonstrate Unknown Fields Preserve
    Given the example table:
      | username | team     |
      | alice    | Platform |
    Then the unknown fields preserve behavior is correct

