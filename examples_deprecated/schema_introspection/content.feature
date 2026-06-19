Feature: Schema introspection

  Scenario: Describe a table contract without parsing records
    Given the content table schema is inspected
    Then its fields and variants are machine readable

