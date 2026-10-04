# -*- coding: UTF-8 -*-

'''
Module
    motion_duplicate_validator.py
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
    Validates consecutive motion targets to detect redundant duplicate motions.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionDuplicateValidator:
    '''
        Validates target coordinates against previous motion target, reporting duplicates.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Compares instruction target coordinates with context last_coords.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'motion_duplicate'

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Checks instruction target coordinates and reports consecutive duplicate motions.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type
        if cmd not in (ScaraCommandType.MOVE_L, ScaraCommandType.MOVE_J):
            context.last_coords = ()
            return ()

        params = instruction.parameters
        x_val = params.get(InstructionParam.X)
        y_val = params.get(InstructionParam.Y)
        z_val = params.get(InstructionParam.Z)
        phi_val = params.get(InstructionParam.PHI, 0.0)

        if x_val is None or y_val is None or z_val is None:
            context.last_coords = ()
            return ()

        coords = (float(x_val), float(y_val), float(z_val), float(phi_val))
        findings: tuple[ScaraDiagnostic, ...] = ()

        if context.last_coords and coords == context.last_coords:
            findings = (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.DUPLICATE_MOTION,
                    severity=ScaraDiagnosticSeverity.INFO,
                    message=(
                        f'Consecutive move to identical target coordinates '
                        f'({coords[0]:.1f}, {coords[1]:.1f}, {coords[2]:.1f}, {coords[3]:.1f}).'
                    ),
                    line=instruction.line_number,
                    command=cmd.value,
                ),
            )

        context.last_coords = coords
        return findings
