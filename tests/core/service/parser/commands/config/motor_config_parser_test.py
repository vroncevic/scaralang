# -*- coding: UTF-8 -*-

'''
Module
    motor_config_parser_test.py
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
    Unit tests for MotorConfigParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType
from scaralang.core.service.parser.commands.config.motor_config_parser import MotorConfigParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotorConfigParser(TestCase):
    '''
        Test cases verifying MotorConfigParser behavior.
    '''

    def test_properties_and_protocol(self) -> None:
        '''Verifies name property and structural protocol conformance.'''
        parser = MotorConfigParser()
        self.assertEqual(parser.name, 'motor_config_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''Verifies can_parse method matches CONFIG_MOTOR and aliases.'''
        parser = MotorConfigParser()
        self.assertTrue(parser.can_parse(command_name='CONFIG_MOTOR'))
        self.assertTrue(parser.can_parse(command_name='MOTOR_MODE'))
        self.assertFalse(parser.can_parse(command_name='SPEED'))
        self.assertFalse(parser.can_parse(command_name='HOME'))

    def test_parse_config_motor_closed_loop(self) -> None:
        '''Verifies parsing of CONFIG MOTOR CLOSED_LOOP instruction.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CLOSED_LOOP', line=1, column=14),
        )
        instruction = parser.parse(
            tokens=tokens, line_num=1, raw_text='CONFIG MOTOR CLOSED_LOOP'
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.CONFIG_MOTOR)
        self.assertEqual(
            instruction.parameters.get(InstructionParam.MODE),
            MotorDriveMode.CLOSED_LOOP.value,
        )
        self.assertEqual(
            instruction.parameters.get(InstructionParam.INTERFACE),
            MotorInterfaceType.CAN_BUS.value,
        )
        self.assertEqual(
            instruction.parameters.get(InstructionParam.AXIS_MASK),
            AxisMask.ALL.value,
        )

    def test_parse_config_motor_open_loop_with_explicit_interface(self) -> None:
        '''Verifies parsing of CONFIG MOTOR OPEN_LOOP with explicit interface.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=2, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=2, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='OPEN_LOOP', line=2, column=14),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='STEP_DIR', line=2, column=24),
        )
        instruction = parser.parse(
            tokens=tokens, line_num=2, raw_text='CONFIG MOTOR OPEN_LOOP STEP_DIR'
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.CONFIG_MOTOR)
        self.assertEqual(
            instruction.parameters.get(InstructionParam.MODE),
            MotorDriveMode.OPEN_LOOP.value,
        )
        self.assertEqual(
            instruction.parameters.get(InstructionParam.INTERFACE),
            MotorInterfaceType.STEP_DIR.value,
        )

    def test_parse_alias_config_motor_with_serial(self) -> None:
        '''Verifies parsing of shorthand CONFIG_MOTOR CLOSED_LOOP SERIAL instruction.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG_MOTOR', line=3, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CLOSED_LOOP', line=3, column=14),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='SERIAL', line=3, column=26),
        )
        instruction = parser.parse(
            tokens=tokens, line_num=3, raw_text='CONFIG_MOTOR CLOSED_LOOP SERIAL'
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.CONFIG_MOTOR)
        self.assertEqual(
            instruction.parameters.get(InstructionParam.INTERFACE),
            MotorInterfaceType.SERIAL.value,
        )

    def test_parse_alias_motor_mode(self) -> None:
        '''Verifies parsing of MOTOR_MODE OPEN_LOOP instruction.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOTOR_MODE', line=4, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='OPEN_LOOP', line=4, column=12),
        )
        instruction = parser.parse(
            tokens=tokens, line_num=4, raw_text='MOTOR_MODE OPEN_LOOP'
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.CONFIG_MOTOR)
        self.assertEqual(
            instruction.parameters.get(InstructionParam.MODE),
            MotorDriveMode.OPEN_LOOP.value,
        )

    def test_parse_syntax_error_too_short(self) -> None:
        '''Verifies ValueError on short CONFIG tokens.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=1, column=8),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG MOTOR')

    def test_parse_alias_syntax_error_too_short(self) -> None:
        '''Verifies ValueError on short alias tokens.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG_MOTOR', line=1, column=1),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG_MOTOR')

    def test_parse_unknown_property(self) -> None:
        '''Verifies ValueError on unknown property under CONFIG.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='UNKNOWN', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CLOSED_LOOP', line=1, column=16),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG UNKNOWN CLOSED_LOOP')

    def test_parse_unexpected_command(self) -> None:
        '''Verifies ValueError on non-matching first keyword.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOVE_L', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CLOSED_LOOP', line=1, column=8),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='MOVE_L CLOSED_LOOP')

    def test_parse_invalid_drive_mode(self) -> None:
        '''Verifies ValueError on invalid drive mode keyword.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='TURBO_LOOP', line=1, column=14),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG MOTOR TURBO_LOOP')

    def test_parse_invalid_interface(self) -> None:
        '''Verifies ValueError on invalid motor interface keyword.'''
        parser = MotorConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='OPEN_LOOP', line=1, column=14),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='ETHERNET', line=1, column=24),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG MOTOR OPEN_LOOP ETHERNET')


if __name__ == '__main__':
    main()
