Feature: CMS CellDSL fallbacks

  Scenario: Fallbacks normalize unmatched values
    Given the example table:
      | IDs    | A-1     |
      | Status | Drafted |
    Then fallback CellDSL rules are applied
