Feature: CMS CellDSL exact tokens

  Scenario: Exact tokens produce generated values
    Given the example table:
      | IDs       | A-1    |
      | Headline* | random |
    Then exact CellDSL tokens are applied
