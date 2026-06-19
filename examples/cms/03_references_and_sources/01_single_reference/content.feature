Feature: Single CMS reference

  Scenario: Resolve one parent reference
    Given the example table:
      | IDs       | ROOT | CHILD       |
      | Headline* | Home | Child story |
      | Parent    |      | ROOT        |
    Then the parent reference resolves to another record
