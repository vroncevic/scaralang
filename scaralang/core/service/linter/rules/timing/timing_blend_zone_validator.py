# -*- coding: UTF-8 -*-

'''
Module
    timing_blend_zone_validator.py
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
    Validates dwell pauses during active continuous blend zones.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
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
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TimingBlendZoneValidator:
    '''
        Validates dwell pauses against active continuous blend zones.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Checks if dwell pause is issued during active continuous blend zone.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'timing_blend_zone'

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
            Checks if dwell pause is issued during active continuous blend zone.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type != ScaraCommandType.WAIT_MS:
            return ()

        if (
            context.zone_mode not in self._EXACT_STOP_MODES
            and context.zone_radius > 0.0
        ):
            return (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.TOOL_IN_FLYBY,
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message='Dwell pause WAIT_MS issued during active continuous blend zone.',
                    line=instruction.line_number,
                    command=ScaraCommandType.WAIT_MS.value,
                ),
            )
        return ()
