Feature: User focused example

  Scenario: Demonstrate Scalar Parsers
    Given the example table:
      | username | age | mask | rating | balance |
      | Alice    | 34  | ff   | 4.5    | 12.30   |
    Then the scalar parsers behavior is correct

