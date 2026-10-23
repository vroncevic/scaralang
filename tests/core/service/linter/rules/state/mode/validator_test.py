# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for ModeValidator operations.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.diagnostic.code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.context.factory import LintContextFactory
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.service.linter.rules.state.mode.validator import ModeValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestModeValidator(TestCase):
    '''
        Test cases verifying ModeValidator operations.

        It defines:

            :methods:
                | test_name - Verifies validator component name.
                | test_non_config_motor_instruction_no_op - Verifies non-CONFIG_MOTOR instruction does not alter context.
                | test_valid_mode_switch_to_closed_loop - Verifies switching to CLOSED_LOOP updates context.
                | test_valid_mode_switch_to_open_loop - Verifies switching to OPEN_LOOP updates context.
                | test_redundant_motor_config - Verifies redundant CONFIG_MOTOR produces INFO diagnostic.
                | test_invalid_motor_mode - Verifies invalid motor mode produces ERROR diagnostic.
    '''

    def test_name(self) -> None:
        '''
            Verifies validator component name.
        '''
        validator = ModeValidator()
        self.assertEqual(validator.name, 'motor_mode_validator')

    def test_non_config_motor_instruction_no_op(self) -> None:
        '''
            Verifies non-CONFIG_MOTOR instruction does not alter context or return diagnostics.
        '''
        validator = ModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=1,
            raw_text='MOVE_L X=10.0',
            parameters={},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 0)

    def test_valid_mode_switch_to_closed_loop(self) -> None:
        '''
            Verifies switching from OPEN_LOOP to CLOSED_LOOP updates context without error.
        '''
        validator = ModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=2,
            raw_text='CONFIG MOTOR CLOSED_LOOP',
            parameters={ScaraInstructionParam.MODE: 'CLOSED_LOOP'},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(len(diagnostics), 0)

    def test_valid_mode_switch_to_open_loop(self) -> None:
        '''
            Verifies switching from CLOSED_LOOP to OPEN_LOOP updates context without error.
        '''
        validator = ModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=3,
            raw_text='CONFIG MOTOR OPEN_LOOP',
            parameters={ScaraInstructionParam.MODE: 'OPEN_LOOP'},
        )
        context = LintContextFactory.create()
        context.motor_drive_mode = MotorDriveMode.CLOSED_LOOP

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 0)

    def test_redundant_motor_config(self) -> None:
        '''
            Verifies redundant CONFIG_MOTOR produces INFO diagnostic.
        '''
        validator = ModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=4,
            raw_text='CONFIG MOTOR OPEN_LOOP',
            parameters={ScaraInstructionParam.MODE: 'OPEN_LOOP'},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.REDUNDANT_MOTOR_CONFIG)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.INFO)
        self.assertEqual(diagnostics[0].line, 4)

    def test_invalid_motor_mode(self) -> None:
        '''
            Verifies invalid motor mode produces ERROR diagnostic.
        '''
        validator = ModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=5,
            raw_text='CONFIG MOTOR INVALID_MODE',
            parameters={ScaraInstructionParam.MODE: 'INVALID_MODE'},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.INVALID_MOTOR_MODE)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertEqual(diagnostics[0].line, 5)


if __name__ == '__main__':
    main()
