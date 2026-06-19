Feature: CMS static checker Python API

  Scenario: Python API finds table diagnostics
    Given the following statically checked content exists:
      | IDs       | A-1          | A-2 |
      | Headline* | Market brief |     |
    Then the Python checker reports structured diagnostics
