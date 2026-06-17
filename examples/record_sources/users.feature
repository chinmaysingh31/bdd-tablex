Feature: Record source metadata

  Scenario: Inspect source cells from a parsed record
    Given the following traceable users exist:
      | name  | role   |
      | Alice | admin  |
      | Bob   | editor |
    Then each user can identify its original table cells
