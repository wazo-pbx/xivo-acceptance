Feature: Stat

    Scenario: Generation of event COMPLETEAGENT
        Given there is no queue with name "q09" or number "5009"
        Given there is no agent with number "009"
        Given there is no user "User" "009"
        Given there is no "COMPLETEAGENT" entry in queue "q09"
        Given there is a user "User" "009" with extension "1009@statscenter"
        Given there is a agent "Agent" "009" with extension "009@statscenter"
        Given there is a queue "q09" with extension "5009@statscenter" with agent "009"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "009" on extension "1009@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I wait call then i answer then i hang up after "2s"
        Given I wait 2 seconds for the calls processing
        Given there is 1 calls to extension "5009@statscenter" and wait
        Given I wait 9 seconds for the calls processing
        Then i should see 1 "COMPLETEAGENT" event in queue "q09" in the queue log