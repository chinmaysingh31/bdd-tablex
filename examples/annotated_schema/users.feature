Feature: Annotation-driven schema conversion

  Scenario: Infer common parsers from field annotations
    Given the following annotated users exist:
      | name  | age | active | tags             |
      | Alice | 30  | yes    | admin, editorial |
      | Bob   |     | no     | viewer           |
    Then annotations produce typed values
