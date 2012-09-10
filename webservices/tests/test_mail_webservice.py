# -*- coding: utf-8 -*-

__license__ = """
    Copyright (C) 2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import unittest
import json
from webservices.webservices import WebServices


class TestMail(unittest.TestCase):
    def setUp(self):
        self._aws = WebServices('configuration/network/mail')

    def tearDown(self):
        reset_data = {
            "mydomain": "",
            "origin": "",
            "relayhost": "",
            "fallback_relayhost": "",
            "canonical": ''
        }

        response = self._aws.edit(reset_data, 0)
        self.assertEqual(response.code, 200)

    def test_edit(self):
        jsonfilecontent = self._aws.get_json_file_content('mail')
        content = json.loads(jsonfilecontent)

        response = self._aws.edit(content, 0)
        self.assertEqual(response.code, 200)

        response = self._aws.view(0)
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
