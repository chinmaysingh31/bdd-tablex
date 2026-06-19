Feature: Alphabetic CMS group expansion

  Scenario: Alphabetic ranges expand grouped content columns
    Given the example table:
      | IDs       | A-C       |
      | Type*     | 3:Article |
      | Headline* | Shared    |
    Then alphabetic group expansion creates one record per ID
