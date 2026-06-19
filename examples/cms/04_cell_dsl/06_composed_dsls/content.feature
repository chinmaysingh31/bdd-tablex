Feature: CMS composed CellDSLs

  Scenario: Composed DSLs use the first matching grammar
    Given the example table:
      | IDs       | A-1        | A-2       | A-3     |
      | Headline* | none       | fake:hero | Literal |
    Then composed CellDSLs are applied in order
