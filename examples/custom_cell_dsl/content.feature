Feature: Project-owned content cell DSL

  Scenario: Parse tokens, patterns, literal values, and empty cells
    Given the following generated content exists:
      | IDs       | 1       | 2       | 3                  |
      | Type*     | Article | Article | Poll               |
      | Headline* | random  | 3 words  | A literal headline |
      | Category  | random  | Markets |                    |
    Then the content table contains the expected normalized values
