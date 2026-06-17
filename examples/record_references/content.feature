Feature: Local record references

  Scenario: Resolve parent and related content IDs
    Given the following linked content exists:
      | IDs      | 1       | 2       | 3       |
      | Headline | Root    | Child   | Other   |
      | Parent   |         | 1       | 1       |
      | Related  | 2, 3    |         | 2       |
    Then local IDs resolve to content records
