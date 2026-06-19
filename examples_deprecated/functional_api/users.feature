Feature: Functional parsing styles

  Scenario: Create users with the pytest fixture style
    Given the following functional API users:
      | name  | role  | active |
      | Alice | admin | true   |
      | Bob   | user  | false  |
