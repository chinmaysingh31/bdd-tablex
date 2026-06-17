Feature: Content variants

  Scenario: Parse different content shapes from one table
    Given the following mixed content exists:
      | IDs       | 1                    | 2                  |
      | Type*     | Article              | Poll               |
      | Headline* | Markets open higher  | Which market leads? |
      | Body*     | A detailed news body |                    |
      | Options*  |                      | Equities, Bonds    |
    Then each content type has its own parsed fields

