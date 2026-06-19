Feature: Variant output models

  Scenario: Convert each variant to its own output model
    Given the example table:
      | IDs       | A-1          | P-1             |
      | Type*     | Article      | Poll            |
      | Headline* | Market brief | Reader question |
      | Body*     | Full text    |                 |
      | Options*  |              | Yes, No         |
    Then variant records become variant output models
