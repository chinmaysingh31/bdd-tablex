Feature: CMS transformer pipeline

  Scenario: Transformer pipelines run left to right
    Given the example table:
      | IDs       | a-1          |
      | Headline* | market brief |
    Then transformer pipelines can normalize source tables
