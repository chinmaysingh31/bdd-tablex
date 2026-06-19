Feature: CMS CLI check JSON

  Scenario: Check a CLI-importable schema and render JSON diagnostics
    Given the following statically checked content exists:
      | IDs       | A-1          | A-2 |
      | Headline* | Market brief |     |
      | Status    | draft        |     |
    Then CLI check JSON uses a plain schema module
