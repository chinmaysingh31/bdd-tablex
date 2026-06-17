Feature: Custom group expansion rules

  Scenario: Use project-defined range and repeat grammar
    Given the following bracket-style content exists:
      | References | R1~R3         | R4    |
      | Kind*      | [3]Article    | Poll  |
      | Headline*  | Regional news | Vote? |
    Then four custom-reference records are produced
