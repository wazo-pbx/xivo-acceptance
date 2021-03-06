# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import schedule_helper, user_helper


@step(u'Given I have a schedule "([^"]*)" in "([^"]*)" with the following schedules:')
def given_i_have_a_schedule_group1_in_group2_with_the_following_schedules(step, name, timezone):
    schedule_helper.add_schedule(name, timezone, step.hashes)


@step(u'Given I have a schedule "([^"]*)" in "([^"]*)" towards user "([^"]*)" "([^"]*)" with the following schedules:')
def given_i_have_a_schedule_group1_in_group2_towards_user_group3_group4_with_the_following_schedules(step, name, timezone, firstname, lastname):
    user = user_helper.get_user_by_name('{} {}'.format(firstname, lastname))
    destination = {'type': 'user', 'user_id': user['id']}
    schedule_helper.add_schedule(name, timezone, step.hashes, destination)
