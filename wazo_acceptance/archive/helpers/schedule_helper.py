# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    has_entries,
)
from lettuce import world

from xivo_acceptance.helpers import entity_helper
from xivo_acceptance.helpers.user_helper import get_by_firstname_lastname


def add_schedule(name, timezone, times, destination=None):
    delete_schedules_with_name(name)
    schedule = _create_schedule(name, timezone, times, destination)
    world.confd_client.schedules.create(schedule)


def assert_schedule_exists(name, timezone, times):
    expected = _create_schedule(name, timezone, times)
    result = find_schedule_by(name=name)
    assert_that(result, has_entries(
        name=expected['name'],
        timezone=expected['timezone'],
        closed_destination=expected['closed_destination'],
        # open_periods=contains_inanyorder(expected['open_periods']),
        # exceptional_periods=contains_inanyorder(expected['exceptional_periods']),
    ))


def expand_number_ranges(collapsed):
    numbers = []
    for range_bloc in collapsed.split(','):
        if '-' in range_bloc:
            low, high = map(int, range_bloc.split('-'))
            numbers += range(low, high+1)
        else:
            numbers.append(int(range_bloc))
    return numbers


def _create_schedule(name, timezone, times, destination=None):
    schedule = {
        'name': name,
        'timezone': timezone,
        'closed_destination': {
            'type': 'none'
        }
    }
    if destination:
        schedule['closed_destination'] = destination

    open_periods, exceptional_periods = [], []
    for time in times:
        period = {
            'hours_end': time['End hour'],
            'hours_start': time['Start hour'],
            'month_days': expand_number_ranges(time['Days of month']),
            'months': expand_number_ranges(time['Months']),
            'week_days': expand_number_ranges(time['Days of week']),
            'destination': _get_destination(time),
        }

        if time['Status'] == 'Opened':
            open_periods.append(period)
        elif time['Status'] == 'Closed':
            exceptional_periods.append(period)

    schedule['open_periods'] = open_periods
    schedule['exceptional_periods'] = exceptional_periods
    return schedule


def _get_destination(time):
    firstname = time.get('Destination firstname')
    lastname = time.get('Destination lastname')

    if not (firstname and lastname):
        return {'type': 'none'}

    user = get_by_firstname_lastname(firstname, lastname)
    return {'type': 'user', 'user_id': user['id']}


def delete_schedules_with_name(name):
    schedules = world.confd_client.schedules.list(name=name)['items']
    for schedule in schedules:
        world.confd_client.schedules.delete(schedule['id'])


def get_schedule_by(**kwargs):
    schedule = find_schedule_by(**kwargs)
    if not schedule:
        raise Exception('Schedule not found: %s' % kwargs)
    return schedule


def find_schedule_by(**kwargs):
    schedules = world.confd_client.schedules.list(**kwargs)['items']
    for schedule in schedules:
        return schedule
