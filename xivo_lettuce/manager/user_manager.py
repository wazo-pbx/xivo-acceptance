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
from xivo_lettuce import common, form, postgres


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


def find_func_key_line(number=None):
    if number:
        number = str(number)
    else:
        number = 'last()'

    xpath = "//tbody[@id='phonefunckey']/tr[%s]" % number
    return world.browser.find_element_by_xpath(xpath)


def find_key_number_field(line):
    return Select(line.find_element_by_name('phonefunckey[fknum][]'))


def find_key_type_field(line):
    return Select(line.find_element_by_name('phonefunckey[type][]'))


def find_key_label_field(line):
    return line.find_element_by_name('phonefunckey[label][]')


def find_key_supervision_field(line):
    return Select(line.find_element_by_name('phonefunckey[supervision][]'))


def add_funckey_line():
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-funckeys']//a[@id='add_funckey_button']")
    add_button.click()


def get_line_number(line):
    element = line.find_element_by_name('phonefunckey[type][]')
    line_number = int(element.get_attribute('id')[-1:])
    return line_number


def find_key_destination_field(key_type, line):
    line_number = get_line_number(line)
    if key_type == 'Filtering Boss - Secretary':
        field_id = 'it-phonefunckey-extenfeatures-bsfilter-typeval-%s' % line_number
    else:
        field_id = 'it-phonefunckey-custom-typeval-%s' % line_number
    return line.find_element_by_id(field_id)


def type_func_key(key_type, destination, key_number=None, label=None, supervised=None):
    go_to_tab('Func Keys')

    add_funckey_line()

    current_line = find_func_key_line()

    key_type_field = find_key_type_field(current_line)
    key_type_field.select_by_visible_text(key_type)

    _fill_destination_field(key_type, current_line, destination)

    if key_number:
        key_number_field = find_key_number_field(current_line)
        key_number_field.select_by_visible_text(key_number)

    if label:
        label_field = find_key_label_field(current_line)
        label_field.send_keys(label)

    if supervised:
        supervision_field = find_key_supervision_field(current_line)
        supervision_field.select_by_visible_text(supervised)


def _fill_destination_field(key_type, line, destination):
    field = find_key_destination_field(key_type, line)
    if key_type == 'Filtering Boss - Secretary':
        Select(field).select_by_visible_text(destination)
    else:
        field.send_keys(destination)


def change_key_order(pairs):
    go_to_tab('Func Keys')
    for old, new in pairs:
        current_line = world.browser.find_element_by_xpath('''//tbody[@id='phonefunckey']/tr[%s]''' % old)
        number_field = Select(current_line.find_element_by_name('phonefunckey[fknum][]'))
        number_field.select_by_visible_text(new)


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


def switchboard_config_for_user(user):
    common.open_url('user')
    common.edit_line(user)
    select_simultaneous_calls(1)
    enable_call_transfer()
    form.submit.submit_form()


def select_simultaneous_calls(nb_calls):
    form.select.set_select_field_with_id("it-userfeatures-simultcalls", str(nb_calls))


def enable_call_transfer():
    go_to_tab("Services")
    form.checkbox.check_checkbox_with_id("it-userfeatures-enablehint")


def count_linefeatures(user_id):
    return _count_table_with_criteria("linefeatures", {"iduserfeatures": user_id})


def count_rightcallmember(user_id):
    return _count_table_with_criteria("rightcallmember", {"type": "'user'", "typeval": "'%s'" % user_id})


def count_dialaction(user_id):
    return _count_table_with_criteria("dialaction", {"category": "'user'", "categoryval": "'%s'" % user_id})


def count_phonefunckey(user_id):
    return _count_table_with_criteria("phonefunckey", {"iduserfeatures": user_id})


def count_callfiltermember(user_id):
    return _count_table_with_criteria("callfiltermember", {"type": "'user'", "typeval": "'%s'" % user_id})


def count_queuemember(user_id):
    return _count_table_with_criteria("queuemember", {"usertype": "'user'", "userid": user_id})


def count_schedulepath(user_id):
    return _count_table_with_criteria("schedule_path", {"path": "'user'", "pathid": user_id})


def _count_table_with_criteria(table, criteria):
    pgcommand = "\"SELECT COUNT(*) FROM %s" % table
    if(criteria is not None and criteria != {}):
        pgcommand += " WHERE "
        for key, value in criteria.iteritems():
            pgcommand += "%s = %s AND " % (key, value)
        pgcommand = pgcommand[:-5]
        pgcommand += "\""
    result = postgres.exec_sql_request_with_return(pgcommand)
    return int(result.split('\n')[-4].strip())


def deactivate_bsfilter(user):
    common.open_url('user', 'search', {'search': user})
    common.edit_line(user)
    common.go_to_tab('Services')
    form.select.set_select_field_with_id('it-userfeatures-bsfilter', 'No')
    form.submit.submit_form()
