# -*- coding: UTF-8 -*-

'''
Module
    instruction_line_parser_test.py
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
    Unit tests for InstructionLineParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.motion.joint_move_command_parser import JointMoveCommandParser
from scaralang.core.service.parser.instruction.instruction_line_parser import InstructionLineParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInstructionLineParser(TestCase):
    '''
        Test cases verifying InstructionLineParser statement dispatch and parsing.

        It defines:

            :methods:
                | test_parse_line_success - Verifies successful parsing of a known command.
                | test_parse_line_empty_tokens - Verifies ValueError on empty token slice.
                | test_parse_line_unknown_command - Verifies ValueError on unregistered command.
                | test_parse_line_cached_dispatch - Verifies cached handler reuse.
                | test_properties - Verifies name and handlers properties.
    '''

    def test_parse_line_success(self) -> None:
        '''
            Verifies successful parsing of a known command.
        '''
        handler = JointMoveCommandParser()
        parser = InstructionLineParser(handlers=(handler,))
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='MOVE_J',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='J1',
                line=1,
                column=8,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='90',
                line=1,
                column=11,
            ),
        )
        instruction = parser.parse_line(tokens=tokens)
        self.assertIsInstance(instruction, ScaraInstruction)
        self.assertEqual(instruction.command_type, ScaraCommandType.MOVE_J)

    def test_parse_line_empty_tokens(self) -> None:
        '''
            Verifies ValueError on empty token slice.
        '''
        parser = InstructionLineParser(handlers=())
        with self.assertRaises(ValueError):
            parser.parse_line(tokens=())

    def test_parse_line_unknown_command(self) -> None:
        '''
            Verifies ValueError on unregistered command.
        '''
        parser = InstructionLineParser(handlers=())
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='UNKNOWN_CMD',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ValueError):
            parser.parse_line(tokens=tokens)

    def test_parse_line_cached_dispatch(self) -> None:
        '''
            Verifies that second invocation uses cached handler.
        '''
        handler = JointMoveCommandParser()
        parser = InstructionLineParser(handlers=(handler,))
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='MOVE_J',
                line=1,
                column=1,
            ),
        )
        inst1 = parser.parse_line(tokens=tokens)
        inst2 = parser.parse_line(tokens=tokens)
        self.assertEqual(inst1.command_type, inst2.command_type)

    def test_properties(self) -> None:
        '''
            Verifies name and handlers properties.
        '''
        handler = JointMoveCommandParser()
        parser = InstructionLineParser(handlers=(handler,))
        self.assertEqual(parser.name, 'instruction_line_parser')
        self.assertEqual(parser.handlers, (handler,))


if __name__ == '__main__':
    main()
