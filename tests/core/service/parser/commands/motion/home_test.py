# -*- coding: UTF-8 -*-

'''
Module
    home_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaralang is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaralang is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for HomeParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.motion.home import HomeParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHomeParser(TestCase):
    '''
        Test cases verifying HomeParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = HomeParser()
        self.assertEqual(parser.name, 'home_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches HOME.
        '''
        parser = HomeParser()
        self.assertTrue(parser.can_parse(command_name='HOME'))
        self.assertFalse(parser.can_parse(command_name='MOVE_L'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of HOME instruction.
        '''
        parser = HomeParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='HOME',
                line=1,
                column=1,
            ),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='HOME')
        self.assertEqual(instruction.command_type, ScaraCommandType.HOME)
        self.assertEqual(instruction.line_number, 1)
        self.assertEqual(instruction.parameters, {})


if __name__ == '__main__':
    main()
