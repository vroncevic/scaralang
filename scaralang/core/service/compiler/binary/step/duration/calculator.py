# -*- coding: UTF-8 -*-

'''
Module
    calculator.py
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
    Calculates execution duration in microseconds for trajectory motion steps.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SegmentDurationCalculator:
    '''
        Calculates execution duration in microseconds for robot motion segments.

        It defines:

            :attributes:
                | IDLE_DURATION_US - Microsecond duration for zero-motion segments.
                | MIN_SPEED_MM_S - Minimum clamping threshold for speed.
                | SPEED_TIME_SCALE - Feedrate scaling factor for duration computation.
                | SEC_TO_US - Conversion factor from seconds to microseconds.
                | MIN_SEGMENT_DURATION_US - Minimum microsecond segment execution floor.
            :methods:
                | __init__ - Initializes SegmentDurationCalculator constructor.
                | calculate_duration - Computes execution duration in microseconds.
                | get_version - Returns implementation version string.
    '''

    IDLE_DURATION_US: ClassVar[int] = 1000
    MIN_SPEED_MM_S: ClassVar[float] = 1.0
    SPEED_TIME_SCALE: ClassVar[float] = 10.0
    SEC_TO_US: ClassVar[float] = 1000000.0
    MIN_SEGMENT_DURATION_US: ClassVar[int] = 5000

    def __init__(self) -> None:
        '''
            Initializes SegmentDurationCalculator constructor.

            :exceptions: None.
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
            :exceptions: None.
        '''
        deltas: tuple[int, int, int, int] = (
            abs(target_steps.j1 - current_steps.j1),
            abs(target_steps.j2 - current_steps.j2),
            abs(target_steps.z - current_steps.z),
            abs(target_steps.j4 - current_steps.j4),
        )
        max_delta: int = max(deltas)

        if max_delta == 0:
            return self.IDLE_DURATION_US

        safe_speed: float = max(self.MIN_SPEED_MM_S, speed_mm_s)
        duration_sec: float = max_delta / (safe_speed * self.SPEED_TIME_SCALE)
        duration_us: int = int(duration_sec * self.SEC_TO_US)

        return max(duration_us, self.MIN_SEGMENT_DURATION_US)

    def get_version(self) -> str:
        '''
            Returns implementation version string.

            :return: Implementation version string.
            :exceptions: None.
        '''
        return __version__
