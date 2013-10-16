# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

from lettuce import step
from xivo_acceptance.helpers.restapi_v1_0.rest_queues import RestQueues
from xivo_acceptance.helpers.restapi_v1_0.rest_campaign import RestCampaign

restqueues = RestQueues()
rest_campaign = RestCampaign()


@step(u'Given there is a queue named "([^"]*)"')
def given_there_is_a_queue_named_group1(step, queue_name):
    assert rest_campaign.queue_create_if_not_exists(queue_name), "Can't add queue"


@step(u'When I create a queue "([^"]*)"')
def when_i_create_a_queue(step, queue_name):
    assert restqueues.create(queue_name)


@step(u'Then I can consult the queue "([^"]*)" and the other ones')
def then_i_can_consult_the_queue_group1_and_the_other_ones(step, queue_name):
    assert restqueues.find("name", queue_name)
