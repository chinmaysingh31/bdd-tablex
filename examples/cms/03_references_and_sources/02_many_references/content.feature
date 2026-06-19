Feature: Many CMS references

  Scenario: Resolve several related content references
    Given the example table:
      | IDs       | A-1     | P-1      | V-1   |
      | Headline* | Article | Poll     | Video |
      | Related   | P-1,V-1 |          | P-1   |
    Then many references resolve in table order
