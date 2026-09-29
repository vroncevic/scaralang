# -*- coding: UTF-8 -*-

'''
Module
    state_zone_validator.py
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
    Validates corner blend zone configurations and updates context state.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StateZoneValidator:
    '''
        Validates ZONE instruction mode and radius, updating simulation context.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Checks ZONE parameters, reports diagnostics, and updates context.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'state_zone'

    _VALID_MODES: tuple[str, ...] = (
        ZoneMode.FINE,
        ZoneMode.EXACT,
        ZoneMode.BLEND,
    )

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Checks ZONE instruction parameters and updates simulation context.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type != ScaraCommandType.ZONE:
            return ()

        params = instruction.parameters
        raw_mode = str(params.get(InstructionParam.MODE, ZoneMode.FINE)).upper()
        radius_val = params.get(
            InstructionParam.RADIUS,
            params.get(InstructionParam.R, 0.0),
        )
        radius = float(radius_val)
        findings: list[ScaraDiagnostic] = []

        if raw_mode not in self._VALID_MODES:
            findings.append(
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.INVALID_ZONE_MODE,
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=(
                        f"Unknown zone mode '{raw_mode}'. "
                        "Expected 'FINE', 'EXACT', or 'BLEND'."
                    ),
                    line=instruction.line_number,
                    command=ScaraCommandType.ZONE.value,
                )
            )

        if radius < 0.0:
            findings.append(
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.INVALID_ZONE_RADIUS,
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=(
                        f'Zone radius {radius:.1f} is negative. '
                        'Expected non-negative radius.'
                    ),
                    line=instruction.line_number,
                    command=ScaraCommandType.ZONE.value,
                )
            )

        context.zone_mode = (
            ZoneMode(raw_mode)
            if raw_mode in self._VALID_MODES
            else ZoneMode.FINE
        )
        context.zone_radius = radius
        return tuple(findings)
