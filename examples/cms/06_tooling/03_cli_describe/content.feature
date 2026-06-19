Feature: CMS CLI describe

  Scenario: Describe a CLI-importable schema
    Given the example table:
      | IDs       | A-1          |
      | Headline* | Market brief |
      | Status    | draft        |
    Then CLI describe uses a plain schema module
