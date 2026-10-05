# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_conflict_validator.py
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
    Validates pneumatic tool actuation to detect pump and valve contention.
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
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PneumaticConflictValidator:
    '''
        Validates whether vacuum pump and blow-off valve contend for simultaneous activation.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Flags contention when both pump and valve are active simultaneously.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'pneumatic_conflict'

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Flags contention when both pump and valve are active simultaneously.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type
        state_val = str(
            instruction.parameters.get(InstructionParam.STATE, PneumaticState.OFF)
        ).upper()
        target_state = state_val == PneumaticState.ON
        conflict_state = (
            context.tool_state.valve_on
            if cmd == ScaraCommandType.PUMP
            else context.tool_state.pump_on
        )

        if not target_state or not conflict_state:
            return ()

        if cmd == ScaraCommandType.PUMP:
            msg = (
                'Cannot turn PUMP ON while blow-off VALVE is active. '
                'Pneumatic contention detected.'
            )
        else:
            msg = (
                'Cannot turn blow-off VALVE ON while vacuum PUMP is active. '
                'Pneumatic contention detected.'
            )

        return (
            ScaraDiagnostic(
                code=ScaraDiagnosticCode.PNEUMATIC_CONFLICT,
                severity=ScaraDiagnosticSeverity.ERROR,
                message=msg,
                line=instruction.line_number,
                command=cmd.value,
            ),
        )
