# -*- coding: utf-8 -*-

import json
import voicemail_manager
from xivo_lettuce.common import get_webservices, go_to_tab
from lettuce.registry import world
from selenium.webdriver.support.select import Select


WSU = get_webservices('user')
WSG = get_webservices('group')


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


def _fill_json_user_data(jsoncontent, data_dict):
    if 'firstname' not in data_dict:
        data_dict['firstname'] = 'firstname'
    if 'lastname' not in data_dict:
        data_dict['lastname'] = 'lastname'
    if 'agentid' not in data_dict:
        data_dict['agentid'] = ''

    return jsoncontent % data_dict


def insert_user_with_no_line(firstname, lastname, agentid=''):
    jsoncontent = WSU.get_json_file_content('user')
    data_dict = {'firstname': firstname,
                 'lastname': lastname,
                 'agentid': agentid}
    datajson = _fill_json_user_data(jsoncontent, data_dict)
    data = json.loads(datajson)
    WSU.add(data)


def insert_user(firstname, lastname, agentid=''):
    jsoncontent = WSU.get_json_file_content('userwithline')
    data_dict = {'firstname': firstname,
                 'lastname': lastname,
                 'agentid': agentid}
    datajson = _fill_json_user_data(jsoncontent, data_dict)
    data = json.loads(datajson)
    WSU.add(data)


def delete_user(firstname, lastname):
    users = world.ws.user.search('%s %s' % (firstname, lastname))
    for user in users:
        if user.voicemail:
            voicemail_manager.delete(user.voicemail.id)
        world.ws.user.delete(user.id)


def delete_all_users():
    WSU.clear()


def find_user_id(firstname, lastname):
    user_list = WSU.list()
    if user_list:
        return [userinfo['id'] for userinfo in user_list if
                userinfo['firstname'] == firstname and userinfo['lastname'] == lastname]
    return []


def is_in_group(group_name, user_id):
    group_list = WSG.list()
    group_id = [group['id'] for group in group_list if group['name'] == group_name]
    if len(group_id) > 0:
        group_view = WSG.view(group_id[0])
        for user in group_view['user']:
            if user['userid'] == user_id:
                return True
    return False


def insert_group_with_user(group_name, user_list=[]):
    data = WSG.get_json_file_content('group')
    users = ""
    if len(user_list) > 0:
        users = r', "user": [%s]' % ', '.join(['"%s"' % str(id) for id in user_list])
    data = data % {'user_list': users,
                   'groupname': group_name}
    data = json.loads(data)
    WSG.clear()
    WSG.add(data)


def user_form_add_line(linenumber):
    go_to_tab('Lines')
    add_button = world.browser.find_element_by_id('lnk-add-row')
    add_button.click()
    input_linenumber = world.browser.find_elements_by_id('linefeatures-number')[-2]
    input_linenumber.send_keys(linenumber)
    go_to_tab('General')
