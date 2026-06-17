Feature: Collected table errors

  Scenario: Report every independent invalid user cell
    Given the following invalid users are checked:
      | name | age   |
      |      | old   |
      |      | older |
    Then four source-aware errors are reported together

