Feature: Inapplicable variant field policies

  Scenario: Preserve a value written for another variant
    Given the example table:
      | IDs       | P-1             |
      | Type*     | Poll            |
      | Headline* | Reader question |
      | Body*     | copied note     |
      | Options*  | Yes, No         |
    Then inapplicable values are preserved as extras
