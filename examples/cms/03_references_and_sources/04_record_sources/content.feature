Feature: CMS record source metadata

  Scenario: Inspect source metadata for parsed records
    Given the example table:
      | IDs       | A-1          |
      | Headline* | Market brief |
      | Status    | draft        |
    Then record sources expose item and field cells
