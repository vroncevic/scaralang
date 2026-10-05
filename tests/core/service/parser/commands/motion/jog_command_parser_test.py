# -*- coding: UTF-8 -*-

'''
Module
    jog_command_parser_test.py
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
    Unit tests for JogCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.motion.jog_command_parser import JogCommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogCommandParser(TestCase):
    '''
        Test cases verifying JogCommandParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_jog_axis_success - Verifies JOG_AXIS statement parsing.
                | test_parse_jog_joint_success - Verifies JOG_JOINT statement parsing.
                | test_parse_invalid_syntax - Verifies ScaraSyntaxError on missing arguments.
                | test_parse_invalid_axis - Verifies ScaraSyntaxError on unknown axis.
                | test_parse_jog_axis_invalid_delta - Verifies ScaraSyntaxError on non-numeric delta.
                | test_parse_jog_joint_invalid_args - Verifies ScaraSyntaxError on invalid joint args.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = JogCommandParser()
        self.assertEqual(parser.name, 'jog_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches JOG_AXIS and JOG_JOINT.
        '''
        parser = JogCommandParser()
        self.assertTrue(parser.can_parse(command_name='JOG_AXIS'))
        self.assertTrue(parser.can_parse(command_name='JOG_JOINT'))
        self.assertFalse(parser.can_parse(command_name='MOVE_L'))

    def test_parse_jog_axis_success(self) -> None:
        '''
            Verifies parsing of JOG_AXIS instruction.
        '''
        parser = JogCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='JOG_AXIS', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='X', line=1, column=10),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='10.5', line=1, column=12),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='JOG_AXIS X 10.5')
        self.assertEqual(instruction.command_type, ScaraCommandType.JOG_AXIS)
        self.assertEqual(instruction.parameters.get(InstructionParam.AXIS), 'X')
        self.assertEqual(instruction.parameters.get(InstructionParam.STEP), 10.5)

    def test_parse_jog_joint_success(self) -> None:
        '''
            Verifies parsing of JOG_JOINT instruction.
        '''
        parser = JogCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='JOG_JOINT', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='1', line=1, column=11),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='5.0', line=1, column=13),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='JOG_JOINT 1 5.0')
        self.assertEqual(instruction.command_type, ScaraCommandType.JOG_JOINT)
        self.assertEqual(instruction.parameters.get(InstructionParam.JOINT), 1)
        self.assertEqual(instruction.parameters.get(InstructionParam.DEG), 5.0)

    def test_parse_invalid_syntax(self) -> None:
        '''
            Verifies ScaraSyntaxError on insufficient tokens.
        '''
        parser = JogCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='JOG_AXIS', line=1, column=1),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='JOG_AXIS')

    def test_parse_invalid_axis(self) -> None:
        '''
            Verifies ScaraSyntaxError on invalid jog axis.
        '''
        parser = JogCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='JOG_AXIS', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='INVALID', line=1, column=10),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='10', line=1, column=18),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='JOG_AXIS INVALID 10')

    def test_parse_jog_axis_invalid_delta(self) -> None:
        '''
            Verifies ScaraSyntaxError on non-numeric jog delta.
        '''
        parser = JogCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='JOG_AXIS', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='X', line=1, column=10),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='BAD_DELTA', line=1, column=12),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='JOG_AXIS X BAD_DELTA')

    def test_parse_jog_joint_invalid_args(self) -> None:
        '''
            Verifies ScaraSyntaxError on non-numeric joint arguments.
        '''
        parser = JogCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='JOG_JOINT', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='BAD_JOINT', line=1, column=11),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='BAD_DEG', line=1, column=21),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='JOG_JOINT BAD_JOINT BAD_DEG')


if __name__ == '__main__':
    main()
