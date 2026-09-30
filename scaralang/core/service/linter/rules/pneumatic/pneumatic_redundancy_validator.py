# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_redundancy_validator.py
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
    Validates pneumatic actuation commands to detect redundant state settings.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PneumaticRedundancyValidator:
    '''
        Validates whether pneumatic actuation commands match the active context state.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Flags redundant actuation commands matching active tool state.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'pneumatic_redundancy'

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Flags redundant actuation commands matching the current state.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type
        tool_name = cmd.value
        state_val = str(
            instruction.parameters.get(InstructionParam.STATE, PneumaticState.OFF)
        ).upper()
        target_state = state_val == PneumaticState.ON
        current_state = (
            context.pump_on
            if cmd == ScaraCommandType.PUMP
            else context.valve_on
        )

        if target_state and current_state:
            return (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.REDUNDANT_TOOL_CMD,
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=f'{tool_name} is already ON. Redundant actuation command.',
                    line=instruction.line_number,
                    command=tool_name,
                ),
            )
        if not target_state and not current_state:
            return (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.REDUNDANT_TOOL_CMD,
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=f'{tool_name} is already OFF. Redundant actuation command.',
                    line=instruction.line_number,
                    command=tool_name,
                ),
            )
        return ()
