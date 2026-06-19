Feature: CMS CellDSL regex patterns

  Scenario: Regex patterns use captured values
    Given the example table:
      | IDs       | A-1    |
      | Headline* | 3:word |
    Then regex CellDSL patterns are applied
