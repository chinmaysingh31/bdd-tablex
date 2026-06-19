Feature: CMS CellDSL predicate rules

  Scenario: Predicate rules handle project-specific syntax
    Given the example table:
      | IDs       | A-1        |
      | Headline* | CMS:launch |
    Then predicate CellDSL rules are applied
