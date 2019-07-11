# wazo-acceptance

wazo-acceptance is a testing framework for running automated tests on a Wazo server.
These tests are used for testing features before releasing a new version of Wazo.


# Style Guide

## Feature file

* Indent with 2 spaces
* In table indent the value to the left
* For other rules, please refer to feature files and then write it here

### Example
```
Feature: Scenarios to test

  Scenario: Description of the scenario
    Given a precondition
    Given a precondition with table
      | long_key_with_a_small_value | key2 |
      | left_indent                 | val2 |
    When something happen
    Then I assert something
```

## Helper file

You should write helper file if you need:
* Have some cleanup
* Wait for asterisk events
* Can be useful for other tests

# Getting Started

## Prerequisites

For Linphone to work, you must do:

    adduser jenkins audio  #Jenkins is the user running the tests


## Configuration

Create a yaml local configuration file in ```~/.wazo-acceptance/config.yml``` and
redefine only options that need to be changed. Default options can be found in
```wazo_acceptance/config.py```. Usually, you will only need to change the IP
addresses. For example:

    default:
      # IP address of the Wazo server
      wazo_host: 192.168.0.10

Configuration path can be changed by passing the following options:

    behave -D acceptance_config_dir=/some/config/path ...
    wazo-acceptance -c /some/config/path ...


## Requirements

We recommend running tests on a dedicated debian machine. Run the following
commands to install requirements:

    apt-get install libsasl2-dev linphone-nogtk python-dev lsof
    pip install -r requirements.txt
    python setup.py install

Once the requirements are installed, modify the configuration files and run the prerequisite script:

    wazo-acceptance -p


## Usage

	usage: wazo-acceptance [-h] [-p] [-v] [-x XIVO_HOST]

	optional arguments:
	  -h, --help            show this help message and exit
	  -p, --prerequisite    execute prerequisite
	  -v, --verbose         verbose mode
	  -x WAZO_HOST, --wazo-host WAZO_HOST
	                        wazo host


# Running tests

Tests can be found in the ```features``` directory. You can run all tests:

    behave features/daily

Or only a single test file:

    behave features/daily/<file>.feature

To see linphone ouput, use flag `--no-capture`


# Coverage

To get code coverage of wazo_acceptance:

    pip install coverage
    coverage run --source=wazo_acceptance $(which behave) ...
    coverage html

# With tox

Tox can be used to wrap all previous examples::

    tox -e setup -- <server_ip>
    tox -e acceptance -- ...
    tox -e behave -- ...
