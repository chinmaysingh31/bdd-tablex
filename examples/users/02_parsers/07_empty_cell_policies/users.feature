Feature: User focused example

  Scenario: Demonstrate Empty Cell Policies
    Given the example table:
      | raw value | parsed value | none value | strict value |
      |           |              |            | filled       |
    Then the empty cell policies behavior is correct

