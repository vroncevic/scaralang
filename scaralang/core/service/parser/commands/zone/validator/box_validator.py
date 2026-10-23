# -*- coding: UTF-8 -*-

'''
Module
    box_validator.py
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
    Implementation of rectangular obstacle zone boundary validator.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BoxZoneValidator:
    '''
        Validates coordinate bounds and parameters for rectangular obstacle zones.

        It defines:

            :cvar REQUIRED_KEYS: Required parameter keys for box zones.
            :methods:
                | __init__ - Initializes BoxZoneValidator instance.
                | validate_parameters - Validates X_MIN, X_MAX, Y_MIN, Y_MAX parameter bounds.
                | get_version - Gets implementation version string.
    '''

    REQUIRED_KEYS: ClassVar[tuple[str, ...]] = (
        ScaraInstructionParam.X_MIN.value,
        ScaraInstructionParam.X_MAX.value,
        ScaraInstructionParam.Y_MIN.value,
        ScaraInstructionParam.Y_MAX.value,
    )

    def __init__(self) -> None:
        '''Initializes BoxZoneValidator instance.'''

    def validate_parameters(
        self,
        *,
        params: dict[str, object],
        line_num: int,
    ) -> None:
        '''
            Validates rectangular box boundary parameters and numerical intervals.

            :param params: Extracted parameter dictionary.
            :param line_num: Source line number for syntax reporting.
            :exceptions:
                | ScaraSyntaxError: If required keys are missing or bounds are invalid.
        '''
        for req_key in self.REQUIRED_KEYS:
            if req_key not in params:
                raise ScaraSyntaxError(
                    f'Missing required parameter {req_key} for BOX zone at line {line_num}'
                )
            val: object = params[req_key]
            if not isinstance(val, (int, float)):
                raise ScaraSyntaxError(
                    f'Parameter {req_key} must be a number at line {line_num}'
                )

        x_min = float(params[ScaraInstructionParam.X_MIN.value])
        x_max = float(params[ScaraInstructionParam.X_MAX.value])
        y_min = float(params[ScaraInstructionParam.Y_MIN.value])
        y_max = float(params[ScaraInstructionParam.Y_MAX.value])

        if x_min >= x_max:
            raise ScaraSyntaxError(
                f'Invalid BOX zone bounds: X_MIN ({x_min}) must be less than '
                f'X_MAX ({x_max}) at line {line_num}'
            )

        if y_min >= y_max:
            raise ScaraSyntaxError(
                f'Invalid BOX zone bounds: Y_MIN ({y_min}) must be less than '
                f'Y_MAX ({y_max}) at line {line_num}'
            )

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
        return __version__
