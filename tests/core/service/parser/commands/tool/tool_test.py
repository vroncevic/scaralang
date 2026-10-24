# -*- coding: UTF-8 -*-

'''
Module
    tool_test.py
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
    Unit tests for ToolParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.tool_position import ToolPosition
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.tool.tool import ToolParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolParser(TestCase):
    '''
        Test cases verifying ToolParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_up_success - Verifies TOOL UP statement parsing.
                | test_parse_down_success - Verifies TOOL DOWN statement parsing.
                | test_parse_missing_arg - Verifies ScaraSyntaxError on missing state.
                | test_parse_invalid_state - Verifies ScaraSyntaxError on invalid state.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = ToolParser()
        self.assertEqual(parser.name, 'tool_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches TOOL.
        '''
        parser = ToolParser()
        self.assertTrue(parser.can_parse(command_name='TOOL'))
        self.assertFalse(parser.can_parse(command_name='PUMP'))

    def test_parse_up_success(self) -> None:
        '''
            Verifies parsing of TOOL UP instruction.
        '''
        parser = ToolParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='TOOL',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='UP',
                line=1,
                column=6,
            ),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='TOOL UP')
        self.assertEqual(instruction.command_type, ScaraCommandType.TOOL)
        self.assertEqual(
            instruction.parameters.get(ScaraInstructionParam.STATE), ToolPosition.UP
        )

    def test_parse_down_success(self) -> None:
        '''
            Verifies parsing of TOOL DOWN instruction.
        '''
        parser = ToolParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='TOOL',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='DOWN',
                line=1,
                column=6,
            ),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='TOOL DOWN')
        self.assertEqual(instruction.command_type, ScaraCommandType.TOOL)
        self.assertEqual(
            instruction.parameters.get(ScaraInstructionParam.STATE),
            ToolPosition.DOWN,
        )

    def test_parse_missing_arg(self) -> None:
        '''
            Verifies ScaraSyntaxError on missing tool state.
        '''
        parser = ToolParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='TOOL',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='TOOL')

    def test_parse_invalid_state(self) -> None:
        '''
            Verifies ScaraSyntaxError on invalid tool state.
        '''
        parser = ToolParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='TOOL',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='ON',
                line=1,
                column=6,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='TOOL ON')


if __name__ == '__main__':
    main()
