Feature: Meetme

    Scenario: Add a conference room
        When I create a conference room with name "red" with number "4000"
        Then meetme "red" is displayed in the list

    Scenario: Add a conference room with max participants set to 0
        When I create a conference room with name "blue" with number "4000" with max participants "0"
        Then meetme "blue" is displayed in the list