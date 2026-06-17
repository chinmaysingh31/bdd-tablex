Feature: Context-aware access validation

  Scenario: Validate users against a project access policy
    Given the following policy-compliant users exist:
      | name  | role   | region |
      | Alice | admin  | global |
      | Bob   | editor | eu     |
    Then the users are accepted by the supplied policy
