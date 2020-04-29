Feature: Creating and removing sources

  Scenario: Creating an image source
    When I view the page
    Then the add button is disabled

    When I select TextContent from the new source dropdown
    Then the add button is enabled

    When I click add
    Then a new text source is added

  Scenario: Deleting an image source
    Given a text source exists
    When I view the page
    And I select the text source
    And I click delete
    Then the text source is removed
