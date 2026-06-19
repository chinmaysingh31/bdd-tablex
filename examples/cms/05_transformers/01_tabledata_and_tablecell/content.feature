Feature: TableData and TableCell

  Scenario: TableData keeps current values and original source values
    Given the example table:
      | IDs       | A-1          |
      | Headline* | Market brief |
    Then TableData and TableCell expose source-aware values
