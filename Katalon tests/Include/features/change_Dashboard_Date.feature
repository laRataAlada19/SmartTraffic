Feature: Change the date for the displaying data in the dashboard
  I want to change the date for the displaying data in the dashboard
  Scenario Outline: Change the date for the displaying data in the dashboard
    Given I start the application
    And I see the Dashboard
    Then I change the date of the displaying data
    Then I close the application