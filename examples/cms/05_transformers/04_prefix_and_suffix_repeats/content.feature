Feature: CMS repeat rules

  Scenario: Prefix and suffix repeat rules create repeated cells
    Given the example table:
      | IDs       | 1..2      |
      | Type*     | 2:Article |
      | Headline* | Shared x2 |
    Then prefix and suffix repeat rules expand values
