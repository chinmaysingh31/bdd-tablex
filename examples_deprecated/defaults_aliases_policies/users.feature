Feature: Defaults, aliases, and additional fields

  Scenario: Evolve a table contract without breaking older wording
    Given the following flexible users:
      | full name | team       |
      | Alice     | Publishing |
    Then missing values are generated and additional values are preserved

