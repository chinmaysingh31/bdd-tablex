Feature: Dataclass output models

  Scenario: Return project domain objects from a BDD table
    Given the following modeled users exist:
      | name  | age |
      | Alice | 30  |
      | Bob   | 24  |
    Then the parsed users are dataclass instances
