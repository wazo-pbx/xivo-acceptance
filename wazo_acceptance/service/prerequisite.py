# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from wazo_acceptance.helpers import context_helper
from wazo_acceptance import setup
from wazo_acceptance import sysutils
from wazo_acceptance.assets import copy_asset_to_server
from xivo_dao.helpers import db_manager  # TODO Remove xivo_dao dependency
from xivo_dao.helpers.db_utils import session_scope


logger = logging.getLogger(__name__)


class Context(object):
    pass


def run(extra_config):
    context = Context()
    logger.debug('Initializing ...')
    setup.setup_config(context, extra_config)
    setup.setup_logging(context)
    setup.setup_wazo_acceptance_config(context)
    setup.setup_ssh_client(context)

    logger.debug('Configuring users external_api')
    _configure_auth_users(context)

    logger.debug('Creating auth client')
    setup.setup_auth_token(context)

    logger.debug('Configuring python clients')
    setup.setup_call_logd_client(context)
    setup.setup_confd_client(context)

    logger.debug('Configuring Consul')
    _configure_consul(context)

    logger.debug('Configuring PostgreSQL on XiVO')
    _configure_postgresql(context)

    logger.debug('Configuring RabbitMQ on XiVO')
    _configure_rabbitmq(context)

    logger.debug('Configuring xivo-agid on XiVO')
    _allow_agid_listen_on_all_interfaces(context)

    logger.debug('Configuring Provd REST API on XiVO')
    _allow_provd_listen_on_all_interfaces(context)

    logger.debug('Installing packages')
    _install_packages(context, ['tcpflow'])

    logger.debug('Installing chan_test (module for asterisk)')
    _install_chan_test(context)

    logger.debug('Installing core_dump program')
    _install_core_dump(context)

    logger.debug('Adding context')
    context_helper.update_contextnumbers_queue(context, 'statscenter', 5000, 5100)
    context_helper.update_contextnumbers_user(context, 'statscenter', 1000, 1100)
    context_helper.update_contextnumbers_user(context, 'default', 1000, 1999)
    context_helper.update_contextnumbers_group(context, 'default', 2000, 2999)
    context_helper.update_contextnumbers_queue(context, 'default', 3000, 3999)
    context_helper.update_contextnumbers_meetme(context, 'default', 4000, 4999)
    context_helper.update_contextnumbers_incall(context, 'from-extern', 1000, 4999, 4)

    logger.debug('Configuring wazo-auth')
    _configure_wazo_service(context, 'wazo-auth')

    logger.debug('Configuring xivo-amid')
    _configure_wazo_service(context, 'xivo-amid')

    logger.debug('Configuring xivo-confd')
    _configure_wazo_service(context, 'xivo-confd')

    logger.debug('Configuring xivo-ctid')
    _configure_wazo_service(context, 'xivo-ctid')

    logger.debug('Configuring wazo-calld')
    _configure_wazo_service(context, 'wazo-calld')


def _configure_postgresql(context):

    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    context.ssh_client.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    context.ssh_client.check_call(cmd)

    hba_file = '/etc/postgresql/9.6/main/pg_hba.conf'
    postgres_conf_file = '/etc/postgresql/9.6/main/postgresql.conf'

    subnet_line = 'host all all {subnet} md5'
    for subnet in context.config['prerequisites']['subnets']:
        _add_line_to_remote_file(context, subnet_line.format(subnet=subnet), hba_file)

    _add_line_to_remote_file(context, "listen_addresses = '*'", postgres_conf_file)

    _restart_service(context, 'postgresql')
    db_manager.init_db(context.config['db_uri'])


def _configure_rabbitmq(context):
    copy_asset_to_server(context, 'rabbitmq.config', '/etc/rabbitmq/rabbitmq.config')
    _restart_service(context, 'rabbitmq-server')


def _configure_auth_users(context):
    _create_auth_user(
        context,
        username='xivo-acceptance',
        password='proformatique',
        acl_templates=[
            'amid.action.*.create',
            'auth.#',
            'confd.#',
            'dird.#',
            'agentd.#',
            'ctid-ng.#',
            'call-logd.#',
            'provd.#',
        ],
    )
    _create_auth_user(
        username='admin',
        password='proformatique',
        acl_templates=[],
    )


def _create_auth_user(context, username, password, acl_templates):
    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'create',
        '--password', password,
        '--purpose', 'external_api',
        username,
    ]
    user_uuid = context.ssh_client.out_call(cmd).decode('utf-8').strip()

    args = []
    if acl_templates:
        args = ['--acl']
        args.extend(acl_templates)

    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'policy',
        'create',
        '{}-policy'.format(username),
    ]
    cmd.extend(args)
    policy_uuid = context.ssh_client.out_call(cmd).decode('utf-8').strip()

    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'add',
        '--policy', policy_uuid,
        user_uuid,
    ]
    context.ssh_client.check_call(cmd)


def _add_line_to_remote_file(context, ssh_client, line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    context.ssh_client.check_call(command)


def _allow_agid_listen_on_all_interfaces(context):
    _add_line_to_remote_file(context, 'listen_address: 0.0.0.0', '/etc/xivo-agid/conf.d/acceptance.yml')


def _allow_provd_listen_on_all_interfaces():
    # TODO use REST API
    with session_scope() as session:
        query = 'UPDATE provisioning SET net4_ip_rest = \'0.0.0.0\''
        session.execute(query)
    # Apply common.conf


def _install_packages(context, packages):
    command = ['apt-get', 'update', '&&', 'apt-get', 'install', '-y']
    command.extend(packages)
    context.ssh_client.check_call(command)


def _install_chan_test(context):
    _install_packages(['make', 'asterisk-dev', 'gcc', 'libc6-dev', 'libssl-dev'])
    command = ['rm', '-rf', '/usr/src/chan-test-master', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['wget', 'https://github.com/wazo-pbx/chan-test/archive/master.zip', '-O', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['unzip', '-d', '/usr/src', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master']
    context.ssh_client.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master', 'install']
    context.ssh_client.check_call(command)


def _install_core_dump(context):
    copy_asset_to_server(context, 'core_dump.c', '/usr/src')
    _install_packages(context, ['gcc'])
    command = ['gcc', '-o', '/usr/local/bin/core_dump', '/usr/src/core_dump.c']
    context.ssh_client.check_call(command)


def _configure_consul(context):
    copy_asset_to_server(context, 'public_consul.json', '/etc/consul/xivo/public_consul.json')
    consul_is_running = sysutils.is_process_running(context, sysutils.get_pidfile_for_service_name('consul'))
    if consul_is_running:
        _restart_service(context, 'consul')


def _configure_wazo_service(context, service):
    _copy_daemon_config_file(service)
    service_is_running = sysutils.is_process_running(context, sysutils.get_pidfile_for_service_name(service))
    if service_is_running:
        _restart_service(context, service)


def _copy_daemon_config_file(context, daemon_name):
    asset_filename = '{}-acceptance.yml'.format(daemon_name)
    remote_path = '/etc/{}/conf.d'.format(daemon_name)
    copy_asset_to_server(context, asset_filename, remote_path)


def _restart_service(context, service_name):
    command = ['systemctl', 'restart', service_name]
    context.ssh_client.check_call(command)
