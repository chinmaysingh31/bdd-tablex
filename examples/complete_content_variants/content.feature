Feature: Complete content variants

  Scenario: Parse a compact mixed-content table
    Given the following complete content table:
      | IDs                | 1..2          | 3                    |
      | Type*              | 2:Article     | Poll                 |
      | Headline*          | 2:random      | Which desk leads?    |
      | Category           | Markets       | Politics             |
      | Published*         | yes           | no                   |
      | Body*              | 2:12:word     |                      |
      | Related            | 3             |                      |
      | Options*           |               | Equities, Bonds      |
      | Closes after hours |               | 24                   |
    Then the complete content records are typed and linked

  Scenario: Convert each content variant to its own output model
    Given the following publish commands:
      | IDs       | A             | P              |
      | Type*     | Article       | Poll           |
      | Headline* | Morning brief | Choose a desk? |
      | Body*     | Full text     |                |
      | Options*  |               | News, Markets  |
    Then each publish command uses its variant output model

