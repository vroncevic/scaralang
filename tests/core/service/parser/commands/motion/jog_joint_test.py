# -*- coding: UTF-8 -*-

'''
Module
    jog_joint_test.py
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
    Unit tests for JogJointParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.motion.jog_joint import JogJointParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogJointParser(TestCase):
    '''
        Test cases verifying JogJointParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies JOG_JOINT statement parsing.
                | test_parse_invalid_syntax - Verifies ScaraSyntaxError on missing arguments.
                | test_parse_invalid_args - Verifies ScaraSyntaxError on non-numeric joint args.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = JogJointParser()
        self.assertEqual(parser.name, 'jog_joint_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches JOG_JOINT.
        '''
        parser = JogJointParser()
        self.assertTrue(parser.can_parse(command_name='JOG_JOINT'))
        self.assertFalse(parser.can_parse(command_name='JOG_AXIS'))
        self.assertFalse(parser.can_parse(command_name='MOVE_L'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of JOG_JOINT instruction.
        '''
        parser = JogJointParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_JOINT',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='1',
                line=1,
                column=11,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='5.0',
                line=1,
                column=13,
            ),
        )
        instruction = parser.parse(
            tokens=tokens, line_num=1, raw_text='JOG_JOINT 1 5.0'
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.JOG_JOINT)
        self.assertEqual(instruction.parameters.get(ScaraInstructionParam.JOINT), 1)
        self.assertEqual(instruction.parameters.get(ScaraInstructionParam.DEG), 5.0)

    def test_parse_invalid_syntax(self) -> None:
        '''
            Verifies ScaraSyntaxError on insufficient tokens.
        '''
        parser = JogJointParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_JOINT',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='JOG_JOINT')

    def test_parse_invalid_args(self) -> None:
        '''
            Verifies ScaraSyntaxError on non-numeric joint arguments.
        '''
        parser = JogJointParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='JOG_JOINT',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='BAD_JOINT',
                line=1,
                column=11,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='BAD_DEG',
                line=1,
                column=21,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(
                tokens=tokens,
                line_num=1,
                raw_text='JOG_JOINT BAD_JOINT BAD_DEG',
            )


if __name__ == '__main__':
    main()
