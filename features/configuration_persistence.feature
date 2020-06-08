Feature: Configuration persists

  Scenario: Configuration change persists
    Given A text source exists
    When I view the page
    And I select the text source
    And I change the name
    Then new name shows up in the list

    When the service is restarted
    And I view the page
    Then the text source has the new name