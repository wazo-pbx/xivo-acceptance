# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from hamcrest import (
    assert_that,
    is_not,
    is_,
    none,
)
from behave import then


@then('the mirror list contains a line matching "{mirror}"')
def then_the_mirror_list_contains_a_line_matching_mirror(context, mirror):
    match = _match_on_mirror_list(context, mirror)
    assert_that(match, is_not(none()))


@then(u'there should be a file name "{filename}"')
def there_should_by_a_file(context, filename):
    filename = _replace_variables(context, filename)
    path = '~/%s' % filename
    assert_that(
        context.remote_sysutils.path_exists(path), is_(True),
        'No such file or directory {}'.format(path),
    )


def _extract_variable(context, pattern, raw_string):
    variable_names = re.findall(pattern, raw_string)
    return {name: getattr(context, name) for name in variable_names}


def _match_on_mirror_list(context, regex):
    output = context.remote_sysutils.output_command(['apt-cache', 'policy'])
    output = output.decode('utf-8')
    return re.search(regex, output)


def _replace_variables(context, raw_string):
    pattern = r'\${(\w+)}'
    mappings = _extract_variable(context, pattern, raw_string)

    def resolve(match):
        variable_name = match.group(0)[2:-1]
        return mappings.get(variable_name)

    return re.sub(pattern, resolve, raw_string)
