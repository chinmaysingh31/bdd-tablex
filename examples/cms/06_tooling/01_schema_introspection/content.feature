Feature: CMS schema introspection

  Scenario: Inspect a CMS schema contract
    Given the example table:
      | IDs       | A-1          |
      | Headline* | Market brief |
      | Status    | draft        |
    Then schema introspection returns a machine-readable contract
