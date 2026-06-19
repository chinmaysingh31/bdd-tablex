Feature: Transformer pipeline

  Scenario: Normalize labels before expanding grouped columns
    Given the following pipelined content:
      | Content IDs | 1..2      |
      | Type        | 2:Article |
    Then both transformer stages have run in order

