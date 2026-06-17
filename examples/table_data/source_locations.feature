Feature: Source-aware table data

  Scenario: Inspect original BDD table cell locations
    Given the following source-aware users exist:
      | name  | status   |
      | Alice | active   |
      | Bob   | disabled |
    Then the table retains its original values and locations
