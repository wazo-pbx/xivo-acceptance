Feature: Agent

    Scenario: Add an agent with first name and last name and remove it
        Given there is no agent with number "23000"
        When I create an agent "Aaliyah" "Stuart" "23000"
        Then agent "Aaliyah Stuart" is displayed in the list of "default" agent group
        When I remove agent "Aaliyah" "Stuart"
        Then agent "Aaliyah Stuart" is not displayed in the list of "default" agent group

    Scenario: Agent modification
        Given an agent "John" "Wayne" "24000" "" in group default
        Then the agent "24000" password is ""
        When I change the agent "24000" password to "8888"
        Then the agent "24000" password is "8888"

    Scenario: Add an agent and logged it
        Given there are no calls running
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "666"
        Given there is a user "User" "666" with extension "1666@default"
        Given there is no agent with number "666"
        When I create an agent "Super" "Agent" "666"
        Then agent "Super Agent" is displayed in the list of "default" agent group
        Given I log agent "666" on extension "1666@default"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "666" in the queue log

    Scenario: Agent search
        Given an agent "Il" "buono" "24000" "" in group default
        Given an agent "Il" "brutto" "25000" "" in group default
        Given an agent "Il" "cattivo" "26000" "" in group default
        When I search an agent "25000"
        Then agent "25000" is displayed in the list of "default" agent group
        When I search an agent "cattivo"
        Then agent "cattivo" is displayed in the list of "default" agent group

    Scenario: Agent group
        When I create an agent group "blue"
        Then agent group "blue" is displayed in the list
        When I create an agent "Bisounours" "Red" "24500" in group "blue"
        Then agent "24500" is displayed in the list of "blue" agent group
        Then agent group "blue" has "1" agents
        When I create an agent group "black"
        When I create an agent "bobi" "cash" "26000" in group "black"
        When I create an agent "toto" "bobo" "26001" in group "black"
        Then agent group "black" has "2" agents
        When I remove agent group "blue"
        Then agent group "blue" is not displayed in the list
        When I create an agent group "green"
        Then agent group "green" is displayed in the list
        When I select a list of agent group "black, green"
        When I remove selected agent group
        Then agent group "black" is not displayed in the list
        Then agent group "green" is not displayed in the list