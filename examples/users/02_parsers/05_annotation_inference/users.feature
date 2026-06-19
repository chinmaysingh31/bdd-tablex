Feature: User focused example

  Scenario: Demonstrate Annotation Inference
    Given the example table:
      | age | ratio | balance | active | status    | tier  | tags     | reviewer | override |
      | 34  | 1.5   | 12.30   | yes    | published | staff | qa, docs |          | many     |
    Then the annotation inference behavior is correct

