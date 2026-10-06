# -*- coding: UTF-8 -*-

'''
Module
    motor_mode_validator.py
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
    Validates motor drive mode configurations and updates context state.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorModeValidator:
    '''
        Validates CONFIG_MOTOR instruction drive mode and updates simulation context.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Checks motor mode, reports diagnostics, and updates context.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'motor_mode_validator'

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Checks CONFIG_MOTOR instruction parameters and updates simulation context.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type != ScaraCommandType.CONFIG_MOTOR:
            return ()

        params = instruction.parameters
        raw_mode: str = str(
            params.get(InstructionParam.MODE, '')
        ).upper()

        if not MotorConfigFactory.is_valid_drive_mode(raw_mode):
            return (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.INVALID_MOTOR_MODE,
                    severity=ScaraDiagnosticSeverity.ERROR,
                    message=(
                        f'Invalid motor drive mode {raw_mode!r}. '
                        f'Must be one of: {MotorConfigFactory.supported_mode_strings()}'
                    ),
                    line=instruction.line_number,
                    command=str(instruction.command_type),
                ),
            )

        target_mode: MotorDriveMode = MotorConfigFactory.parse_drive_mode(raw_mode)
        findings: list[ScaraDiagnostic] = []

        if context.motor_drive_mode == target_mode:
            findings.append(
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.REDUNDANT_MOTOR_CONFIG,
                    severity=ScaraDiagnosticSeverity.INFO,
                    message=(
                        f'Motor drive mode is already set to {target_mode.value}.'
                    ),
                    line=instruction.line_number,
                    command=str(instruction.command_type),
                )
            )

        context.motor_drive_mode = target_mode

        return tuple(findings)
