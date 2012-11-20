# -*- coding: utf-8 -*-
import time
from lettuce import step, world
from xivo_lettuce.manager import provd_general_manager as provd
from xivo_lettuce.common import open_url

PROXY_FIELDS = ['http_proxy', 'ftp_proxy', 'https_proxy']

@step(u'Given I have no proxies configured')
def given_i_have_no_proxies_configured(step):
    host, port = provd.rest_api_configuration()
    provd.rest_put(host, port, "/provd/configure/http_proxy", None)
    provd.rest_put(host, port, "/provd/configure/ftp_proxy", None)
    provd.rest_put(host, port, "/provd/configure/https_proxy", None)


@step(u'When I configure the following proxies:')
def when_i_configure_the_following_proxies(step):
    open_url('provd_general')
    for config in step.hashes:
        provd.configure_proxies(config)

@step(u'When I reload the provisionning general settings page')
def when_i_reload_the_provisionning_general_settings_page(step):
    open_url('provd_general')


@step(u'When I remove all proxy configurations')
def when_i_remove_all_proxy_configurations(step):
    for field in PROXY_FIELDS:
        element = world.browser.find_element_by_name(field)
        element.clear()
        element.send_keys("\b")
        time.sleep(3)


@step(u'Then there are no proxies configured')
def then_there_are_no_proxies_configured(step):
    for field in PROXY_FIELDS:
        element = world.browser.find_element_by_name(field)
        value = element.get_attribute('value')
        assert value == ""

