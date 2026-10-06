# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_lint_rule.py
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
    Validates vacuum pump and blow-off valve state consistency, contention, and flyby safety.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.pneumatic.ipneumatic_conflict_validator import IPneumaticConflictValidator
from scaralang.core.service.linter.rules.pneumatic.ipneumatic_flyby_validator import IPneumaticFlybyValidator
from scaralang.core.service.linter.rules.pneumatic.ipneumatic_redundancy_validator import IPneumaticRedundancyValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PneumaticLintRule:
    '''
        Lint rule checking pneumatic pump/valve contention, redundant states,
        and zone blend violations.

        It defines:

            :attributes:
                | _flyby_validator - IPneumaticFlybyValidator collaborator.
                | _redundancy_validator - IPneumaticRedundancyValidator collaborator.
                | _conflict_validator - IPneumaticConflictValidator collaborator.
            :methods:
                | __init__ - Initializes PneumaticLintRule with injected validators.
                | name - Returns rule identifier name.
                | check - Evaluates instruction against pneumatic state and blend config.
    '''

    _flyby_validator: IPneumaticFlybyValidator
    _redundancy_validator: IPneumaticRedundancyValidator
    _conflict_validator: IPneumaticConflictValidator

    def __init__(
        self,
        *,
        flyby_validator: IPneumaticFlybyValidator,
        redundancy_validator: IPneumaticRedundancyValidator,
        conflict_validator: IPneumaticConflictValidator,
    ) -> None:
        '''
            Initializes PneumaticLintRule with injected collaborating validators.

            :param flyby_validator: Required IPneumaticFlybyValidator instance.
            :param redundancy_validator: Required IPneumaticRedundancyValidator instance.
            :param conflict_validator: Required IPneumaticConflictValidator instance.
            :exceptions: None.
        '''
        self._flyby_validator: Final[IPneumaticFlybyValidator] = flyby_validator
        self._redundancy_validator: Final[IPneumaticRedundancyValidator] = redundancy_validator
        self._conflict_validator: Final[IPneumaticConflictValidator] = conflict_validator

    @property
    def name(self) -> str:
        '''
            Returns the rule identifier name.

            :return: Rule identifier name string.
            :exceptions: None.
        '''
        return 'pneumatic'

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Evaluates pneumatic instructions, returning findings and updating context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type

        if cmd not in (ScaraCommandType.PUMP, ScaraCommandType.VALVE):
            return ()

        findings: list[ScaraDiagnostic] = []
        findings.extend(
            self._flyby_validator.validate(
                instruction=instruction,
                context=context,
            )
        )
        findings.extend(
            self._redundancy_validator.validate(
                instruction=instruction,
                context=context,
            )
        )
        findings.extend(
            self._conflict_validator.validate(
                instruction=instruction,
                context=context,
            )
        )

        state_val = str(
            instruction.parameters.get(InstructionParam.STATE, PneumaticState.OFF)
        ).upper()
        target_state = state_val == PneumaticState.ON

        if cmd == ScaraCommandType.PUMP:
            context.tool_state.pump_on = target_state
        else:
            context.tool_state.valve_on = target_state

        context.last_coords = ()
        return tuple(findings)
