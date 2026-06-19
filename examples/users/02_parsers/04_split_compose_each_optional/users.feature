Feature: User focused example

  Scenario: Demonstrate Split Compose Each Optional
    Given the example table:
      | tags         | scores | reviewer |
      | qa, docs     | 1;2;3  | none     |
    Then the split compose each optional behavior is correct

