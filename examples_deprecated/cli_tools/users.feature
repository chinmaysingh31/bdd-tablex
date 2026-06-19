Feature: CLI table tooling

  Scenario: Invalid users are reported before test execution
    Given the following CLI users:
      | name  | age |
      |       | old |
