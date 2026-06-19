Feature: CMS CellDSL diagnostics

  Scenario: DSL handler errors keep source diagnostics
    Given the example table:
      | IDs       | A-1    |
      | Headline* | broken |
    Then DSL errors report the original cell
