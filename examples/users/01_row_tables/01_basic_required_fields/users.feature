Feature: User focused example

  Scenario: Demonstrate Basic Required Fields
    Given the example table:
      | username | email             | active |
      | alice    | alice@example.com | true   |
    Then the basic required fields behavior is correct

