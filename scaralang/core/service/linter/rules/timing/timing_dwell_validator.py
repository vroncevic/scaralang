# -*- coding: UTF-8 -*-

'''
Module
    timing_dwell_validator.py
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
    Validates dwell timing delays to detect non-positive wait durations.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TimingDwellValidator:
    '''
        Validates dwell duration on WAIT_MS instructions.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Checks if delay parameter is non-positive and emits DEAD_WAIT.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'timing_dwell'

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Checks delay parameter and returns DEAD_WAIT diagnostic if non-positive.

            :param instruction: Primitive AST instruction node.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type != ScaraCommandType.WAIT_MS:
            return ()

        params = instruction.parameters
        delay_ms: float = float(params.get(InstructionParam.MS, 0.0))

        if delay_ms <= 0.0:
            return (
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.DEAD_WAIT,
                    severity=ScaraDiagnosticSeverity.INFO,
                    message=(
                        f'Dwell delay WAIT_MS {delay_ms:.0f} is '
                        f'non-positive and produces no pause.'
                    ),
                    line=instruction.line_number,
                    command=ScaraCommandType.WAIT_MS.value,
                ),
            )
        return ()
