Feature: User focused example

  Scenario: Demonstrate Split Compose Each Optional
    Given The following users are present
      | name  | age | roles               | active |
      | Akash | 27  | Developer,Manager   | Yes    |
      | Badal | 25  | Tester,Scrum Master | No     |
    Then the split compose each optional behavior is correct
