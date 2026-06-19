Feature: Users

  Scenario: Create users from a row-oriented table
    Given the following users exist:
      | name  | role   | active |
      | Alice | admin  | true   |
      | Bob   | editor | false  |
