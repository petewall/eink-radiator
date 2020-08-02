Feature: Controller page
  Scenario: Content on the page
    When I view the page
    Then I can see the current image
    And I can see the preview image
    And I can see the list of image sources

    When I select the red image source
    Then the preview image goes red

    When I click the "set image" button
    Then the screen image goes red
