Feature: Stat

    Scenario: Generation of event COMPLETECALLER
        Given there are no calls running
        Given there is no "COMPLETECALLER" entry in queue "q08"
        Given there is a user "User" "008" with extension "1008@statscenter"
        Given there is a agent "Agent" "008" with extension "008@statscenter"
        Given there is a queue "q08" with extension "5008@statscenter" with agent "008"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "008" on extension "1008@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I wait call then I answer after "2s" then I wait
        Given I wait 2 seconds for the calls processing
        Given there is 1 calls to extension "5008@statscenter" then I hang up after "5s"
        Given I wait 10 seconds for the calls processing
        Then I should see 1 "COMPLETECALLER" event in queue "q08" in the queue log
