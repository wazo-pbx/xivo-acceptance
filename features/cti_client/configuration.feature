Feature: CtiClient Configuration

    Scenario: Bad server address
        When I start the XiVO Client
        When I log in the XiVO Client with bad server address
        Then I see a error message on CtiClient

    Scenario: Bad server port
        When I start the XiVO Client
        When I log in the XiVO Client with bad server port
        Then I see a error message on CtiClient

    Scenario: Show/Hide agent option on login screen
        When I start the XiVO Client
        When I hide agent option on login screen
        Then I not see agent option on login screen
        When I show agent option on login screen
        Then I see agent option on login screen

    Scenario: Client doesn't crash after disconnecting
        Given there is a profile "full" with no services and xlets:
        | xlet                    | position |
        | Identity                | dock     |
        | Dialer                  | dock     |
        | History                 | dock     |
        | Search                  | dock     |
        | Directory               | dock     |
        | Fax                     | dock     |
        | Features                | dock     |
        | Conference rooms        | dock     |
        | Datetime                | dock     |
        | Tabber                  | grid     |
        | MyDirectory             | dock     |
        | Customer info           | dock     |
        | Agents (list)           | dock     |
        | Agents (detail)         | dock     |
        | Queues (list)           | dock     |
        | Queue members           | dock     |
        | Queues (entries detail) | dock     |
        | Switchboard             | dock     |
        | Remote directory        | dock     |
        | Agent status dashboard  | dock     |
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Bernard   | Derome   | 1044   | default | full        |
        When I start the XiVO Client
        When I log in and log out of the XiVO Client as "bernard", pass "derome" 10 times
        Then the XiVO Client did not crash
