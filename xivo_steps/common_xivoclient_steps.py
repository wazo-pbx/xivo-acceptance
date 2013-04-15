# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import socket
import errno
from lettuce import step, world
from xivo_lettuce.xivoclient import run_xivoclient
from xivo_lettuce import common
from xivo_lettuce.manager_ws import user_manager_ws
from xivo_lettuce.manager import cti_client_manager
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to


@step(u'When I start the XiVO Client')
def i_start_the_xivo_client(step):
    run_xivoclient()

    try:
        world.xc_socket.connect('/tmp/xivoclient')
    except socket.error as(error_number, message):
        world.xc_process.terminate()
        if error_number == errno.ENOENT:
            raise Exception('XiVO Client must be built for functional testing')
        else:
            raise message


@step(u'Then I get sheet infos')
def get_sheet_infos(step):
    cti_client_manager.get_sheet_infos()


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()

    assert_that(world.xc_response, equal_to('passed'))


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)", unlogged agent$')
def i_log_in_the_xivo_client_as_1_pass_2_unlogged_agent(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password,
        'agent_option': 'unlogged'
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()

    assert_that(world.xc_response, equal_to('passed'))


@step(u'I log out of the XiVO Client$')
def log_out_of_the_xivo_client(step):
    cti_client_manager.log_out_of_the_xivo_client()

    assert_that(world.xc_response, equal_to('passed'))


@step(u'When I disable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_disable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.disable_cti_client(firstname, lastname)


@step(u'When I enable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_enable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.enable_cti_client(firstname, lastname)


@step(u'Then I can\'t connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_t_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    cti_client_manager.log_user_in_client(firstname, lastname)
    assert_that(world.xc_response, equal_to('passed'))


@step(u'Then I can connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    cti_client_manager.log_user_in_client(firstname, lastname)
    assert_that(world.xc_response, equal_to('passed'))
