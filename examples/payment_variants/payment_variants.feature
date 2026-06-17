Feature: Payment output variants

  Scenario: Build different domain models from row variants
    Given the following payments were received:
      | type | amount | last_four | account |
      | card | 25     | 4242      |         |
      | bank | 50     |           | QA-001  |
    Then payment variants become their own domain models

