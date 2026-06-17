Feature: Reusable field parsers

  Scenario: Convert product cells into useful Python values
    Given the following typed products exist:
      | sku  | price | active | tags             | priority |
      | A-1  | 12.50 | yes    | news, featured   | high     |
      | B-2  | 7.00  | no     | archive          | low      |
    Then product values are converted and composed
