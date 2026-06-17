Feature: Alphabetic project table transformation

  Scenario: Expand alphabetic keys and x-style repeated values
    Given the following compact alphabetic content exists:
      | Keys      | A-C           | D      |
      | Kind*     | Article x3    | Poll   |
      | Headline* | Regional news | Vote?  |
    Then four alphabetic content records are produced
