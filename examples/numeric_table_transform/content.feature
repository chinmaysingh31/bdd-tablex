Feature: Numeric project table transformation

  Scenario: Expand numeric ID ranges and repeated values
    Given the following compact numeric content exists:
      | IDs       | 1..3            | 4                   |
      | Type*     | 3:Article       | Poll                |
      | Headline* | Shared headline | Is the market open? |
    Then four numeric content records are produced
