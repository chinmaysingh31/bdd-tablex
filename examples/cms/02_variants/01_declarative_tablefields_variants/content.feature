Feature: Declarative CMS variants

  Scenario: Select variants declared with TableFields
    Given the example table:
      | IDs       | A-1          | P-1             |
      | Type*     | Article      | Poll            |
      | Headline* | Market brief | Reader question |
      | Body*     | Full text    |                 |
      | Options*  |              | Yes, No         |
    Then declarative variants produce typed records
