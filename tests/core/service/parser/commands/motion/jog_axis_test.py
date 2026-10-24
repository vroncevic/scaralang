# -*- coding: UTF-8 -*-

'''
Module
    jog_axis_test.py
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
    Unit tests for JogAxisParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.motion.jog_axis import JogAxisParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogAxisParser(TestCase):
    '''
        Test cases verifying JogAxisParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies JOG_AXIS statement parsing.
                | test_parse_invalid_syntax - Verifies ScaraSyntaxError on missing arguments.
                | test_parse_invalid_axis - Verifies ScaraSyntaxError on unknown axis.
                | test_parse_invalid_delta - Verifies ScaraSyntaxError on non-numeric delta.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = JogAxisParser()
        self.assertEqual(parser.name, 'jog_axis_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches JOG_AXIS.
        '''
        parser = JogAxisParser()
        self.assertTrue(parser.can_parse(command_name='JOG_AXIS'))
        self.assertFalse(parser.can_parse(command_name='JOG_JOINT'))
        self.assertFalse(parser.can_parse(command_name='MOVE_L'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of JOG_AXIS instruction.
        '''
        parser = JogAxisParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_AXIS',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='X',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='10.5',
                line=1,
                column=12,
            ),
        )
        instruction = parser.parse(
            tokens=tokens, line_num=1, raw_text='JOG_AXIS X 10.5'
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.JOG_AXIS)
        self.assertEqual(instruction.parameters.get(ScaraInstructionParam.AXIS), 'X')
        self.assertEqual(
            instruction.parameters.get(ScaraInstructionParam.STEP), 10.5
        )

    def test_parse_invalid_syntax(self) -> None:
        '''
            Verifies ScaraSyntaxError on insufficient tokens.
        '''
        parser = JogAxisParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_AXIS',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='JOG_AXIS')

    def test_parse_invalid_axis(self) -> None:
        '''
            Verifies ScaraSyntaxError on invalid jog axis.
        '''
        parser = JogAxisParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_AXIS',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='INVALID',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='10',
                line=1,
                column=18,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(
                tokens=tokens, line_num=1, raw_text='JOG_AXIS INVALID 10'
            )

    def test_parse_invalid_delta(self) -> None:
        '''
            Verifies ScaraSyntaxError on non-numeric jog delta.
        '''
        parser = JogAxisParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_AXIS',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='X',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='BAD_DELTA',
                line=1,
                column=12,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(
                tokens=tokens, line_num=1, raw_text='JOG_AXIS X BAD_DELTA'
            )


if __name__ == '__main__':
    main()
