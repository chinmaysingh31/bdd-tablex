Feature: User focused example

  Scenario: Demonstrate Boolean Custom Vocabulary
    Given the example table:
      | default active | lifecycle active | strict active |
      | yes            | enabled          | YES           |
      | off            | inactive         | NO            |
    Then the boolean custom vocabulary behavior is correct

