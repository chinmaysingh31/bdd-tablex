Feature: Output factories

  Scenario: Build a project object with parse context
    Given the following output-factory users:
      | name  |
      | Alice |
    Then the custom output builder receives the record and context

