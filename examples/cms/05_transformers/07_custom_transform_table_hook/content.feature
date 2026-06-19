Feature: Custom transform_table hook

  Scenario: A schema can override transform_table directly
    Given the example table:
      | IDs       | A-1   |
      | Headline* | draft |
    Then custom transform_table hooks can rewrite logical cells
