Feature: Setting the screen image
  Scenario: Setting the screen image
    Given A text source exists
    When I view the page
    And I select the text source
    And I change the text
    And I click save
    Then the preview image shows the text image

    When I click the "set image" button
    Then the screen image shows the same image
