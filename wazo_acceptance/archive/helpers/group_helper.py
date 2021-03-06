# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def add_or_replace_group(name, exten='2000', context='default', users=None):
    delete_groups_with_number(exten, context)
    _delete_groups_with_name(name)
    add_group(name, exten, context, users)


def add_group(name, exten, context='default', users=None):
    extension = {'exten': exten, 'context': context}
    extension = world.confd_client.extensions.create(extension)

    group = {'name': name}
    group = world.confd_client.groups.create(group, tenant_uuid=extension['tenant_uuid'])

    world.confd_client.groups(group).add_extension(extension)

    if users:
        world.confd_client.groups(group).update_user_members(users)


def delete_groups_with_number(exten, context='default'):
    extensions = world.confd_client.extensions.list(exten=exten,
                                                    context=context,
                                                    recurse=True)['items']
    for extension in extensions:
        if extension['group']:
            world.confd_client.groups.delete(extension['group']['id'])
        world.confd_client.extensions.delete(extension['id'])


def _delete_groups_with_name(name):
    groups = world.confd_client.groups.list(name=name)['items']
    for group in groups:
        world.confd_client.groups.delete(group['id'])
        for extension in group['extensions']:
            world.confd_client.extensions.delete(extension['id'])


def get_group_by_name(name):
    groups = world.confd_client.groups.list(name=name)['items']
    if len(groups) != 1:
        raise Exception('expecting 1 group with name %r; found %s' %
                        (name, len(groups)))
    return groups[0]
