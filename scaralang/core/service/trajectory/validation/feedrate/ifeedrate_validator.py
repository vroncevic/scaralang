# -*- coding: UTF-8 -*-

'''
Module
    ifeedrate_validator.py
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
    Defines structural protocol IFeedrateValidator for feedrate limit validation.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.trajectory.validation_result import ValidationResult

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFeedrateValidator(Protocol):
    '''
        Protocol defining feedrate boundary validation contract.

        It defines:

            :attributes:
                | name - Identifier name of the feedrate validator.
            :methods:
                | validate_feedrate - Validates feedrate within safe mechanical limits.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the feedrate validator identifier name.

            :return: Validator name string.
        '''

    def validate_feedrate(self, speed: float) -> ValidationResult:
        '''
            Validates whether the feedrate is within safe mechanical limits.

            :param speed: Linear speed in mm/s.
            :return: ValidationResult with status and details.
        '''
