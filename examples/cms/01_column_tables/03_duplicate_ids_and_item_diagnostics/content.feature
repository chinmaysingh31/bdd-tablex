Feature: Duplicate CMS item IDs

  Scenario: Duplicate item IDs report the offending item
    Given the example table:
      | IDs       | A-1          | A-1            |
      | Type*     | Article      | Poll           |
      | Headline* | Market brief | Duplicate poll |
    Then duplicate IDs are reported with item diagnostics
