# -*- coding: UTF-8 -*-

'''
Module
    repeat_test.py
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
    Unit tests for RepeatParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.macro.repeat import RepeatParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestRepeatParser(TestCase):
    '''
        Test cases verifying RepeatParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing with integer or key-value.
                | test_parse_missing_count - Verifies ScaraSyntaxError on missing count.
                | test_parse_invalid_count - Verifies ScaraSyntaxError on invalid count values.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.

            :exceptions: None.
        '''
        parser = RepeatParser()
        self.assertIsInstance(parser, ICommandParser)
        self.assertEqual(parser.name, 'repeat_parser')

    def test_can_parse(self) -> None:
        '''
            Verifies command matching logic.

            :exceptions: None.
        '''
        parser = RepeatParser()
        self.assertTrue(parser.can_parse(command_name='REPEAT'))
        self.assertFalse(parser.can_parse(command_name='DEF'))
        self.assertFalse(parser.can_parse(command_name='MOVE_L'))

    def test_parse_success(self) -> None:
        '''
            Verifies successful parsing of REPEAT statements.

            :exceptions: None.
        '''
        parser = RepeatParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='REPEAT',
                line=3,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='5',
                line=3,
                column=8,
            ),
        )
        instruction = parser.parse(
            tokens=tokens,
            line_num=3,
            raw_text='REPEAT 5',
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.REPEAT)
        self.assertEqual(instruction.line_number, 3)
        self.assertEqual(
            instruction.parameters.get(ScaraInstructionParam.COUNT),
            5,
        )

        tokens_kv = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='REPEAT',
                line=4,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='COUNT=10',
                line=4,
                column=8,
            ),
        )
        inst_kv = parser.parse(
            tokens=tokens_kv,
            line_num=4,
            raw_text='REPEAT COUNT=10',
        )
        self.assertEqual(
            inst_kv.parameters.get(ScaraInstructionParam.COUNT),
            10,
        )

    def test_parse_missing_count(self) -> None:
        '''
            Verifies ScaraSyntaxError on missing count.

            :exceptions: None.
        '''
        parser = RepeatParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='REPEAT',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='REPEAT')

        tokens_extra = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='REPEAT',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='5',
                line=1,
                column=8,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='EXTRA',
                line=1,
                column=10,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens_extra, line_num=1, raw_text='REPEAT 5 EXTRA')

    def test_parse_invalid_count(self) -> None:
        '''
            Verifies ScaraSyntaxError on invalid count values.

            :exceptions: None.
        '''
        parser = RepeatParser()
        tokens_bad = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='REPEAT',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='ABC',
                line=1,
                column=8,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens_bad, line_num=1, raw_text='REPEAT ABC')

        tokens_zero = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='REPEAT',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='0',
                line=1,
                column=8,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens_zero, line_num=1, raw_text='REPEAT 0')


if __name__ == '__main__':
    main()
