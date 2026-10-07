# -*- coding: UTF-8 -*-

'''
Module
    motor_mode_validator_test.py
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
    Unit tests for MotorModeValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.service.linter.rules.state.motor_mode_validator import MotorModeValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotorModeValidator(TestCase):
    '''
        Test cases verifying MotorModeValidator operations.
    '''

    def test_name(self) -> None:
        '''
            Verifies validator component name.
        '''
        validator = MotorModeValidator()
        self.assertEqual(validator.name, 'motor_mode_validator')

    def test_non_config_motor_instruction_no_op(self) -> None:
        '''
            Verifies non-CONFIG_MOTOR instruction does not alter context or return diagnostics.
        '''
        validator = MotorModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=1,
            raw_text='MOVE_L X=10.0',
            parameters={},
        )
        context = ScaraLintContext(motor_drive_mode=MotorDriveMode.OPEN_LOOP)

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 0)

    def test_valid_mode_switch_to_closed_loop(self) -> None:
        '''
            Verifies switching from OPEN_LOOP to CLOSED_LOOP updates context without error.
        '''
        validator = MotorModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=2,
            raw_text='CONFIG MOTOR CLOSED_LOOP',
            parameters={InstructionParam.MODE: 'CLOSED_LOOP'},
        )
        context = ScaraLintContext(motor_drive_mode=MotorDriveMode.OPEN_LOOP)

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(len(diagnostics), 0)

    def test_valid_mode_switch_to_open_loop(self) -> None:
        '''
            Verifies switching from CLOSED_LOOP to OPEN_LOOP updates context without error.
        '''
        validator = MotorModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=3,
            raw_text='CONFIG MOTOR OPEN_LOOP',
            parameters={InstructionParam.MODE: 'OPEN_LOOP'},
        )
        context = ScaraLintContext(motor_drive_mode=MotorDriveMode.CLOSED_LOOP)

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 0)

    def test_redundant_motor_config(self) -> None:
        '''
            Verifies redundant CONFIG_MOTOR produces INFO diagnostic.
        '''
        validator = MotorModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=4,
            raw_text='CONFIG MOTOR OPEN_LOOP',
            parameters={InstructionParam.MODE: 'OPEN_LOOP'},
        )
        context = ScaraLintContext(motor_drive_mode=MotorDriveMode.OPEN_LOOP)

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
        validator = MotorModeValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=5,
            raw_text='CONFIG MOTOR INVALID_MODE',
            parameters={InstructionParam.MODE: 'INVALID_MODE'},
        )
        context = ScaraLintContext(motor_drive_mode=MotorDriveMode.OPEN_LOOP)

        diagnostics = validator.validate(instruction=instruction, context=context)

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.INVALID_MOTOR_MODE)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertEqual(diagnostics[0].line, 5)


if __name__ == '__main__':
    main()
