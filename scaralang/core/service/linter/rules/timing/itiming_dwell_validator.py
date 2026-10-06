# -*- coding: UTF-8 -*-

'''
Module
    itiming_dwell_validator.py
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
    Defines structural protocol ITimingDwellValidator for dwell delay duration validation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITimingDwellValidator(Protocol):
    '''
        Structural protocol defining contracts for dwell delay validation.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Validates dwell delay duration on WAIT_MS instructions.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
        '''

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Checks dwell delay parameter, reporting dead waits for non-positive values.

            :param instruction: Primitive AST instruction node.
            :return: Tuple of detected ScaraDiagnostic findings.
        '''
