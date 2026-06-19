Feature: Variant-specific CMS validation

  Scenario: Article validation runs only for article records
    Given the example table:
      | IDs       | A-1     | P-1      |
      | Type*     | Article | Poll     |
      | Headline* | Brief   | Question |
      | Body*     | short   |          |
      | Options*  |         | Yes, No  |
    Then variant validation reports article policy errors
