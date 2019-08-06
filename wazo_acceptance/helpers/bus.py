# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import functools
import queue
import threading
from contextlib import contextmanager

logger = logging.getLogger(__name__)
tasks = None


class Bus:

    def __init__(self, context):
        self._context = context
        self._websocketd_client = context.websocketd_client
        self._websocket_thread = None
        self._received_events = None

    @contextmanager
    def wait_for_asterisk_reload(self, dialplan=False, pjsip=False, queue=False):
        commands = []
        if dialplan:
            commands.append('dialplan reload')
        if pjsip:
            commands.append('module reload res_pjsip.so')
        if queue:
            commands.append('module reload app_queue.so')

        if not commands:
            raise Exception('No wait module specified')

        with self._wait_for_asterisk_reload(commands):
            yield

    @contextmanager
    def _wait_for_asterisk_reload(self, reload_commands):
        global tasks
        tasks = {command: None for command in reload_commands}

        def asterisk_reload(data):
            global tasks
            command = data['command']
            if command not in tasks:
                return

            task_uuid = data['uuid']
            if data['status'] == 'starting':
                tasks[command] = task_uuid
            elif data['status'] == 'completed' and task_uuid in tasks.values():
                tasks.pop(command)
                if not tasks:
                    # TODO expose close method on wazo-websocketd-client
                    self._websocketd_client._ws_app.close()

        self._websocketd_client.on('asterisk_reload_progress', asterisk_reload)
        self._start()
        try:
            yield
        finally:
            self._websocket_thread.join(timeout=5)
            if self._websocket_thread.is_alive():
                logger.warning('No event received for %s', reload_commands)
            self._stop()

    def subscribe(self, events):
        for event in events:
            self._websocketd_client.on(
                event,
                functools.partial(self._save_event, event)
            )
        self._start()
        self._context.add_cleanup(self._stop)

    def _save_event(self, name, data):
        self._received_events.put({'name': name, 'data': data})

    def pop_received_event(self, timeout=5):
        if self._websocket_thread is None:
            raise RuntimeError("websocket thread not started")
        return self._received_events.get(timeout=timeout)

    def _start(self):
        if self._websocket_thread:
            raise RuntimeError("websocket thread already started")
        self._received_events = queue.Queue()
        self._websocket_thread = threading.Thread(target=self._websocketd_client.run)
        self._websocket_thread.start()

    def _stop(self):
        if self._websocket_thread.is_alive():
            self._websocketd_client._ws_app.close()
            self._websocket_thread.join()
        # TODO allow to remove callback on wazo-websocketd-client
        self._websocketd_client._callbacks.clear()
        self._websocketd_client._ws_app = None
        self._websocketd_client._is_running = None
        self._received_events = None
        self._websocket_thread = None