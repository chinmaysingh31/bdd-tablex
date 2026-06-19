Feature: Content record validation

  Scenario: Validate relationships between parsed content fields
    Given the following validated content exists:
      | IDs       | 1             | 2                   |
      | Type*     | Article       | Poll                |
      | Headline* | Market update | Is the market open? |
      | Category  | Markets       |                     |
    Then both content records pass their schema rules
