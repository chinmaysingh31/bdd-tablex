Feature: Explicit CMS variant classes

  Scenario: Select variants registered with decorators
    Given the example table:
      | IDs       | A-1          | V-1           |
      | Type*     | Article      | Video         |
      | Headline* | Market brief | Launch clip   |
      | Body*     | Full text    |               |
      | URL*      |              | /launch-video |
    Then explicit variant classes produce typed records
