Feature: CMS CellDSL field-scoped rules

  Scenario: Field scopes keep tokens local to one field
    Given the example table:
      | IDs       | A-1    |
      | Headline* | random |
      | Status    | random |
    Then field-scoped CellDSL rules affect only selected fields
