# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_flyby_validator.py
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
    Validates that pneumatic tool actions do not occur during active continuous blend zones.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PneumaticFlybyValidator:
    '''
        Validates whether pneumatic actuation occurs within continuous blend zones.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Checks context blend mode and emits TOOL_IN_FLYBY diagnostic.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'pneumatic_flyby'

    _EXACT_STOP_MODES: tuple[ZoneMode, ...] = (
        ZoneMode.FINE,
        ZoneMode.EXACT,
    )

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Checks if tool command was issued during continuous blend flyby zone.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if (
            context.zone_mode not in self._EXACT_STOP_MODES
            and context.zone_radius > 0.0
        ):
            cmd_val = instruction.command_type.value
            return (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.TOOL_IN_FLYBY,
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=(
                        f'Tool action {cmd_val} issued during '
                        f'active continuous blend zone.'
                    ),
                    line=instruction.line_number,
                    command=cmd_val,
                ),
            )
        return ()
