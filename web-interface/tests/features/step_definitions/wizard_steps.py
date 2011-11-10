# -*- coding: utf-8 -*-

from lettuce import step
from lettuce import world


@step(u'Given that there is a XiVO installed at (.*)')
def given_that_there_is_a_xivo_installed_at(step, ip):
    world.ip = ip

@step(u'When I start the wizard')
def when_i_start_the_wizard(step):
    world.browser.get(world.ip)

@step(u'Then I should see the welcome message (.*)')
def then_i_see_the_welcome_message(step, message):
    world.browser.implicitly_wait(2)
    assert message in world.browser.page_source

@step(u'When I select language (.*)')
def when_i_select(step, language):
    language_option = world.browser.find_element_by_xpath('//option[@value="%s"]' %(language))
    language_option.click()

@step(u'When I click next')
def when_i_click_next(step):
    world.browser.find_element_by_id('it-next').click()

@step(u'Then I should be on the licence page')
def then_i_should_be_on_the_licence_page(step):
    world.browser.implicitly_wait(2)
    assert 'Licence' in world.browser.page_source

@step(u'When I accept the terms of the licence')
def when_i_accept_the_terms_of_the_licence(step):
    accept_box = world.browser.find_element_by_id('it-license-agree')
    accept_box.click()

@step(u'Then I should be on the ipbx page')
def then_i_should_be_on_the_ipbx_page(step):
    world.browser.implicitly_wait(2)
    assert 'IPBX engine' in world.browser.page_source

@step(u'Then I should be on the DB page')
def then_i_should_be_on_the_db_page(step):
    world.browser.implicitly_wait(2)
    assert u'Database' in world.browser.page_source
