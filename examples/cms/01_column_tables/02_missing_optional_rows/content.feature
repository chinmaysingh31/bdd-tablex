Feature: Missing optional CMS rows

  Scenario: Parse content when an optional row is absent
    Given the example table:
      | IDs       | A-1          | P-1             |
      | Type*     | Article      | Poll            |
      | Headline* | Market brief | Reader question |
    Then missing optional rows become None
