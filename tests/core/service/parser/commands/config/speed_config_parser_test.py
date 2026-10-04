# -*- coding: UTF-8 -*-

'''
Module
    speed_config_parser_test.py
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
    Unit tests for SpeedConfigParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.config.speed_config_parser import SpeedConfigParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpeedConfigParser(TestCase):
    '''
        Test cases verifying SpeedConfigParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
                | test_parse_invalid_syntax - Verifies ValueError on missing parameters.
                | test_parse_invalid_mode - Verifies ValueError on invalid speed mode.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = SpeedConfigParser()
        self.assertEqual(parser.name, 'speed_config_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches SPEED.
        '''
        parser = SpeedConfigParser()
        self.assertTrue(parser.can_parse(command_name='SPEED'))
        self.assertFalse(parser.can_parse(command_name='ACCEL'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of SPEED instruction.
        '''
        parser = SpeedConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='SPEED', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='WORK', line=1, column=7),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='100.0', line=1, column=12),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='SPEED WORK 100.0')
        self.assertEqual(instruction.command_type, ScaraCommandType.SPEED)
        self.assertEqual(instruction.parameters.get(InstructionParam.MODE), SpeedMode.WORK)
        self.assertEqual(instruction.parameters.get(InstructionParam.SPEED), 100.0)

    def test_parse_invalid_syntax(self) -> None:
        '''
            Verifies ValueError on short tokens.
        '''
        parser = SpeedConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='SPEED', line=1, column=1),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='SPEED')

    def test_parse_invalid_mode(self) -> None:
        '''
            Verifies ValueError on invalid speed mode.
        '''
        parser = SpeedConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='SPEED', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='TURBO', line=1, column=7),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='100.0', line=1, column=13),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='SPEED TURBO 100.0')


if __name__ == '__main__':
    main()
