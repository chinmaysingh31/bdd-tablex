Feature: Composable project syntax

  Scenario: Combine shared and field-specific cell rules
    Given the following composable content:
      | headline  | category |
      | random    | random   |
      | fake:poll | none     |
    Then the first matching scoped or composed rule is used

