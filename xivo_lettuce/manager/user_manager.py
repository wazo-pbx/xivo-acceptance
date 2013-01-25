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

import time
from xivo_lettuce.common import go_to_tab
from lettuce.registry import world
from selenium.webdriver.support.select import Select
from xivo_lettuce import common, form


def type_user_names(firstName, lastName):
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User form not loaded')
    input_firstName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firstName.clear()
    input_firstName.send_keys(firstName)
    input_lastName.clear()
    input_lastName.send_keys(lastName)


def type_user_in_group(groupName):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-6']//a[@href='#groups']")
    group.click()
    world.browser.find_element_by_id('sb-part-groups', 'Group tab not loaded')
    select_group = world.browser.find_element_by_xpath('//select[@id="it-grouplist"]//option[@value="%s"]' % groupName)
    select_group.click()
    add_button = world.browser.find_element_by_id('bt-ingroup')
    add_button.click()


def type_func_key(func_key_kind, destination):
    go_to_tab('Func Keys')
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-funckeys']//a[@id='add_funckey_button']")
    add_button.click()
    type_field = Select(world.browser.find_element_by_id('it-phonefunckey-type-1'))
    type_field.select_by_visible_text(func_key_kind)
    destination_field = world.browser.find_element_by_id('it-phonefunckey-custom-typeval-1')
    destination_field.send_keys(destination)


def user_form_add_line(linenumber, context='default'):
    go_to_tab('Lines')
    add_button = world.browser.find_element_by_id('lnk-add-row')
    add_button.click()
    input_context = world.browser.find_elements_by_id('linefeatures-context')[-2]
    input_context.send_keys(context)
    input_linenumber = world.browser.find_elements_by_id('linefeatures-number')[-2]
    input_linenumber.send_keys(linenumber)
    go_to_tab('General')


def type_voicemail(voicemail_number):
    common.go_to_tab('General')
    form.select.set_select_field_with_label('Language', 'en_US')
    common.go_to_tab('Voicemail')
    form.select.set_select_field_with_label('Voice Mail', 'Asterisk')
    form.input.set_text_field_with_label('Voicemail', voicemail_number)


def type_mobile_number(mobile_number):
    common.go_to_tab('General')
    form.input.set_text_field_with_label('Mobile phone number', mobile_number)


def remove_line():
    common.go_to_tab('Lines')
    select_line = world.browser.find_element_by_xpath("//table[@id='list_linefeatures']/tbody/tr//input[@id='linefeatures-number']")
    delete_button = select_line.find_element_by_xpath("//a[@title='Delete this line']")
    delete_button.click()
    time.sleep(world.timeout)
