# -*- coding: UTF-8 -*-

'''
Module
    icalculator.py
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
    Structural protocol for trajectory step execution duration calculation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISegmentDurationCalculator(Protocol):
    '''
        Structural protocol defining motion step segment duration calculation.

        It defines:

            :methods:
                | calculate_duration - Computes execution duration in microseconds.
                | get_version - Returns implementation version string.
    '''

    def calculate_duration(
        self,
        *,
        current_steps: JointStepCoordinates,
        target_steps: JointStepCoordinates,
        speed_mm_s: float,
    ) -> int:
        '''
            Computes segment execution duration in microseconds.

            :param current_steps: Initial joint step coordinates.
            :param target_steps: Target joint step coordinates.
            :param speed_mm_s: Planned linear tool speed in mm/s.
            :return: Microsecond execution duration.
        '''

    def get_version(self) -> str:
        '''
            Returns implementation version string.

            :return: Implementation version string.
        '''
