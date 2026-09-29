# -*- coding: UTF-8 -*-

'''
Module
    wait_command_parser_test.py
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
    Unit tests for WaitCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.flow.wait_command_parser import WaitCommandParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaitCommandParser(TestCase):
    '''
        Test cases verifying WaitCommandParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_wait_success - Verifies WAIT statement parsing.
                | test_parse_wait_ms_success - Verifies WAIT_MS statement parsing.
                | test_parse_missing_arg - Verifies ValueError on missing duration.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = WaitCommandParser()
        self.assertEqual(parser.name, 'wait_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches WAIT and WAIT_MS.
        '''
        parser = WaitCommandParser()
        self.assertTrue(parser.can_parse(command_name='WAIT'))
        self.assertTrue(parser.can_parse(command_name='WAIT_MS'))
        self.assertFalse(parser.can_parse(command_name='HOLD'))

    def test_parse_wait_success(self) -> None:
        '''
            Verifies parsing of WAIT instruction.
        '''
        parser = WaitCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='WAIT', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='250', line=1, column=6),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='WAIT 250')
        self.assertEqual(instruction.command_type, ScaraCommandType.WAIT_MS)
        self.assertEqual(instruction.parameters.get('ms'), 250.0)

    def test_parse_wait_ms_success(self) -> None:
        '''
            Verifies parsing of WAIT_MS instruction.
        '''
        parser = WaitCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='WAIT_MS', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='500', line=1, column=9),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='WAIT_MS 500')
        self.assertEqual(instruction.command_type, ScaraCommandType.WAIT_MS)
        self.assertEqual(instruction.parameters.get('ms'), 500.0)

    def test_parse_missing_arg(self) -> None:
        '''
            Verifies ValueError on missing delay argument.
        '''
        parser = WaitCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='WAIT', line=1, column=1),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='WAIT')


if __name__ == '__main__':
    main()
