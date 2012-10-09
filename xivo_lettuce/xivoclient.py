# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import json
from lettuce import before, after, world


def run_xivoclient():
    xc_path = os.environ['XC_PATH'] + '/'
    environment_variables = os.environ
    environment_variables['LD_LIBRARY_PATH'] = '.'
    world.xc_process = subprocess.Popen('./xivoclient',
                                        cwd=xc_path,
                                        env=environment_variables)


def xivoclient_step(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(step, *kargs):
        formatted_command = _format_command(f.__name__, kargs)
        _send_and_receive_command(formatted_command)
        print 'XC response: %s %r' % (f.__name__, world.xc_response)
        f(step, *kargs)
    return xivoclient_decorator


def xivoclient(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(*kargs):
        formatted_command = _format_command(f.__name__, kargs)
        _send_and_receive_command(formatted_command)
        print 'XC response: %s %r' % (f.__name__, world.xc_response)
        f(*kargs)
    return xivoclient_decorator


def _format_command(function_name, arguments):
    command = {'function_name': function_name,
               'arguments': arguments}
    formatted_command = json.dumps(command)
    return formatted_command


def _send_and_receive_command(formatted_command):
    world.xc_socket.send('%s\n' % formatted_command)
    world.xc_response = str(world.xc_socket.recv(1024))


@before.each_scenario
def setup_xivoclient_rc(scenario):
    world.xc_process = None
    world.xc_socket = socket.socket(socket.AF_UNIX)


@after.each_scenario
def clean_xivoclient_rc(scenario):
    if world.xc_process:
        world.xc_process.poll()
        if world.xc_process.returncode is None:
            i_stop_the_xivo_client()


@xivoclient
def i_stop_the_xivo_client():
    assert world.xc_response == "OK"