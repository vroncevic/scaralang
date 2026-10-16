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
    Calculates execution duration and axis peak step counts for binary steps.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.joint_step_coordinates import JointStepCoordinates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MetricsCalculator:
    '''
        Calculates execution duration and axis peak step counts for binary steps.

        It defines:

            :attributes:
                | ZERO_DURATION - Initial duration metric accumulator.
                | INITIAL_PEAK_VALUE - Initial peak step displacement metric.
                | AXIS_COUNT - Total degrees of freedom for the manipulator arm.
                | MICROSECONDS_PER_SECOND - Unit conversion factor from us to seconds.
            :methods:
                | calculate_metrics - Computes total duration and peak step counts.
                | calculate_telemetry - Computes comprehensive binary execution telemetry.
                | get_version - Gets implementation version string.
    '''

    ZERO_DURATION: ClassVar[int] = 0
    INITIAL_PEAK_VALUE: ClassVar[int] = 0
    AXIS_COUNT: ClassVar[int] = 4
    MICROSECONDS_PER_SECOND: ClassVar[float] = 1_000_000.0

    def calculate_metrics(
        self, *, steps: Sequence[BinaryStep]
    ) -> tuple[int, JointStepCoordinates]:
        '''
            Computes total duration in microseconds and peak axis step counts.

            :param steps: Sequence of BinaryStep instances.
            :return: Tuple of (total_duration_us, JointStepCoordinates peak steps).
            :exceptions: None.
        '''
        total_duration: int = self.ZERO_DURATION
        peak_j1: int = self.INITIAL_PEAK_VALUE
        peak_j2: int = self.INITIAL_PEAK_VALUE
        peak_z: int = self.INITIAL_PEAK_VALUE
        peak_j4: int = self.INITIAL_PEAK_VALUE

        for s in steps:
            total_duration += s.duration_us
            peak_j1 = max(peak_j1, abs(s.target_steps.j1))
            peak_j2 = max(peak_j2, abs(s.target_steps.j2))
            peak_z = max(peak_z, abs(s.target_steps.z))
            peak_j4 = max(peak_j4, abs(s.target_steps.j4))

        return total_duration, JointStepCoordinates(
            j1=peak_j1,
            j2=peak_j2,
            z=peak_z,
            j4=peak_j4,
        )

    def calculate_telemetry(
        self, *, steps: Sequence[BinaryStep], raw_bytes: bytes
    ) -> BinaryProgramTelemetry:
        '''
            Computes comprehensive binary execution telemetry and axis step metrics.

            :param steps: Sequence of BinaryStep instances.
            :param raw_bytes: Compiled binary raw byte sequence.
            :return: BinaryProgramTelemetry domain model.
            :exceptions: None.
        '''
        total_duration, peak_steps = self.calculate_metrics(steps=steps)
        duration_s: float = total_duration / self.MICROSECONDS_PER_SECOND

        return BinaryProgramTelemetry(
            source_instructions=len(steps),
            compiled_steps=len(steps),
            duration_us=total_duration,
            duration_s=duration_s,
            peak_steps=AxisPeakSteps(
                peak_j1_steps=peak_steps.j1,
                peak_j2_steps=peak_steps.j2,
                peak_z_steps=peak_steps.z,
                peak_j4_steps=peak_steps.j4,
            ),
            total_wire_bytes=len(raw_bytes),
        )

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
