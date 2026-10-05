# -*- coding: UTF-8 -*-

'''
Module
    tool_orient_command_parser_test.py
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
    Unit tests for ToolOrientCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.commands.config.tool_orient_command_parser import ToolOrientCommandParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolOrientCommandParser(TestCase):
    '''
        Test cases verifying ToolOrientCommandParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies TOOL_ORIENT statement parsing.
                | test_parse_missing_mode - Verifies ValueError on missing mode.
                | test_parse_invalid_mode - Verifies ValueError on invalid mode.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = ToolOrientCommandParser()
        self.assertEqual(parser.name, 'tool_orient_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches TOOL_ORIENT.
        '''
        parser = ToolOrientCommandParser()
        self.assertTrue(parser.can_parse(command_name='TOOL_ORIENT'))
        self.assertFalse(parser.can_parse(command_name='TOOL'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of TOOL_ORIENT instruction.
        '''
        parser = ToolOrientCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='TOOL_ORIENT', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='FIXED', line=1, column=13),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='PHI', line=1, column=19),
            ScaraToken(token_type=ScaraTokenType.EQUALS, value='=', line=1, column=22),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='45', line=1, column=23),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='TOOL_ORIENT FIXED PHI=45')
        self.assertEqual(instruction.command_type, ScaraCommandType.TOOL_ORIENT)
        self.assertEqual(instruction.parameters.get(InstructionParam.MODE), ToolOrientMode.FIXED)
        self.assertEqual(instruction.parameters.get(InstructionParam.PHI), 45.0)

    def test_parse_missing_mode(self) -> None:
        '''
            Verifies ScaraSyntaxError on missing mode.
        '''
        parser = ToolOrientCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='TOOL_ORIENT', line=1, column=1),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='TOOL_ORIENT')

    def test_parse_invalid_mode(self) -> None:
        '''
            Verifies ScaraSyntaxError on invalid mode.
        '''
        parser = ToolOrientCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='TOOL_ORIENT', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='INVALID_MODE', line=1, column=13),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='TOOL_ORIENT INVALID_MODE')


if __name__ == '__main__':
    main()
