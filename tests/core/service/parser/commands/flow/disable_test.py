# -*- coding: UTF-8 -*-

'''
Module
    disable_test.py
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
    Unit tests for DisableParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.flow.disable import DisableParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDisableParser(TestCase):
    '''
        Test cases verifying DisableParser behavior.

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
        parser = DisableParser()
        self.assertEqual(parser.name, 'disable_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches DISABLE.
        '''
        parser = DisableParser()
        self.assertTrue(parser.can_parse(command_name='DISABLE'))
        self.assertFalse(parser.can_parse(command_name='ENABLE'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of DISABLE instruction.
        '''
        parser = DisableParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='DISABLE',
                line=1,
                column=1,
            ),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='DISABLE')
        self.assertEqual(instruction.command_type, ScaraCommandType.DISABLE)
        self.assertEqual(instruction.line_number, 1)
        self.assertEqual(instruction.parameters, {})


if __name__ == '__main__':
    main()
