Feature: Basic CMS column table

  Scenario: Parse a basic CMS column table
    Given the example table:
      | IDs       | A-1          | P-1             |
      | Type*     | Article      | Poll            |
      | Headline* | Market brief | Reader question |
      | Status    | draft        | published       |
    Then the column table records are parsed by item column
