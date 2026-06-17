Feature: Reusable field components

  Scenario: Reuse audit fields in an article table
    Given the following audited articles exist:
      | headline | created_by | trace_id |
      | News     | Alice      | trace-1  |
    Then the article contains its reusable audit fields
