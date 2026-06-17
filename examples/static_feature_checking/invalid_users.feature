Feature: Static feature checking

  Scenario: Invalid users are found before scenario execution
    Given the following statically checked users:
      | name | age |
      |      | old |

