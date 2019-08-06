# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ConfdUser:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        ring_seconds = body.pop('ring_seconds', None)
        if ring_seconds:
            body['ring_seconds'] = int(ring_seconds)

        user = self._confd_client.users.create(body)
        self._context.add_cleanup(self._confd_client.users.delete, user)
        return user

    def add_line(self, user, line):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True, pjsip=True):
            self._confd_client.users(user).add_line(line)
        self._context.add_cleanup(self._confd_client.users(user).remove_line, line)

    def add_voicemail(self, user, voicemail_id):
        confd_user = self._confd_client.users(user)
        confd_user.add_voicemail(voicemail_id)
        self._context.add_cleanup(confd_user.remove_voicemail)

    def get_by(self, **kwargs):
        user = self._find_by(**kwargs)
        if not user:
            raise Exception('Confd user not found: {}'.format(kwargs))
        return user

    def _find_by(self, **kwargs):
        users = self._confd_client.users.list(**kwargs)['items']
        for user in users:
            return user