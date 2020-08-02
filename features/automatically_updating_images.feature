Feature: Image sources that auto-update
  Scenario: Image sources that auto-update
    Given A slideshow source exists
    When I view the page
    And I select the slideshow source
    And I set two image URLs
    And I change the interval to 1 second
    And I click the "set image" button

    Then the screen shows the first image

    When I wait for 1.5 seconds
    And I view the page
    Then the screen image shows the second image
