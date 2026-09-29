# -*- coding: UTF-8 -*-

'''
Module
    feedrate_validator.py
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
    Validates tool feedrate against robot mechanical speed limits.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.trajectory.validation_result import ValidationResult

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FeedrateValidator:
    '''
        Validates feedrate against mechanical speed limits.

        It defines:

            :attributes:
                | name - Identifier name of the feedrate validator.
                | _bounds - Kinematic parameters of the SCARA arm.
            :methods:
                | __init__ - Initializes validator with robot bounds.
                | validate_feedrate - Validates that speed is within safe mechanical range.
    '''

    _bounds: ScaraBounds

    def __init__(self, bounds: ScaraBounds) -> None:
        '''
            Initializes feedrate validator using injected robot bounds model.

            :param bounds: ScaraBounds instance.
        '''
        self._bounds: Final[ScaraBounds] = bounds

    @property
    def name(self) -> str:
        '''
            Gets the feedrate validator identifier name.

            :return: Validator name string.
        '''
        return 'feedrate_validator'

    def validate_feedrate(self, speed: float) -> ValidationResult:
        '''
            Validates that speed is within safe mechanical operation range.

            :param speed: Feedrate in mm/s.
            :return: ValidationResult with status and details.
        '''
        if speed < self._bounds.min_speed:
            return ValidationResult(
                is_valid=False,
                message=(
                    f'Speed {speed:.1f} mm/s is too slow '
                    f'(minimum {self._bounds.min_speed:.1f} mm/s)'
                ),
                error_index=-1,
            )

        if speed > self._bounds.max_speed:
            return ValidationResult(
                is_valid=False,
                message=(
                    f'Speed {speed:.1f} mm/s exceeds max safe feedrate '
                    f'{self._bounds.max_speed:.1f} mm/s'
                ),
                error_index=-1,
            )

        return ValidationResult(is_valid=True, message='Speed is valid', error_index=-1)
