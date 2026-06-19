Feature: Typed CMS ID references

  Scenario: Reference keys use the target ID parser
    Given the example table:
      | IDs       | 101  | 102   |
      | Headline* | Home | Child |
      | Parent    |      | 101   |
    Then typed ID references resolve using parsed IDs
