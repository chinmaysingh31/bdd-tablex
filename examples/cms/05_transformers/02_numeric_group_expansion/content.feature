Feature: Numeric CMS group expansion

  Scenario: Numeric ranges expand grouped content columns
    Given the example table:
      | IDs       | 1..3      |
      | Type*     | 3:Article |
      | Headline* | Shared    |
    Then numeric group expansion creates one record per ID
