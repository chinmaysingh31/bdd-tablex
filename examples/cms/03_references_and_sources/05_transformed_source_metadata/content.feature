Feature: Transformed CMS source metadata

  Scenario: Expanded grouped columns preserve original source cells
    Given the example table:
      | IDs       | 1..2      |
      | Headline* | 2:Shared  |
    Then transformed records still point at compact source cells
