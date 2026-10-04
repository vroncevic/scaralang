# -*- coding: UTF-8 -*-

'''
Module
    binary_metrics_calculator.py
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

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.step import Step

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryMetricsCalculator:
    '''
        Calculates execution duration and axis peak step counts for binary steps.

        It defines:

            :methods:
                | calculate_metrics - Computes total duration and peak step counts.
                | calculate_telemetry - Computes comprehensive binary execution telemetry.
    '''

    def calculate_metrics(
        self, *, steps: Sequence[Step]
    ) -> tuple[int, tuple[int, int, int, int]]:
        '''
            Computes total duration in microseconds and peak axis step counts.

            :param steps: Sequence of Step instances.
            :return: Tuple of (total_duration_us, (peak_j0, peak_j1, peak_z, peak_pitch)).
            :exceptions: None.
        '''
        total_duration: int = 0
        peak_steps: list[int] = [0, 0, 0, 0]

        for s in steps:
            total_duration += s.duration_us

            for i in range(4):
                if abs(s.target_steps[i]) > peak_steps[i]:
                    peak_steps[i] = abs(s.target_steps[i])

        return total_duration, (
            peak_steps[0],
            peak_steps[1],
            peak_steps[2],
            peak_steps[3],
        )

    def calculate_telemetry(
        self, *, steps: Sequence[Step], raw_bytes: bytes
    ) -> BinaryProgramTelemetry:
        '''
            Computes comprehensive binary execution telemetry and axis step metrics.

            :param steps: Sequence of Step instances.
            :param raw_bytes: Compiled binary raw byte sequence.
            :return: BinaryProgramTelemetry domain model.
            :exceptions: None.
        '''
        total_duration, peak_steps = self.calculate_metrics(steps=steps)
        duration_s: float = total_duration / 1000000.0

        return BinaryProgramTelemetry(
            source_instructions=len(steps),
            compiled_steps=len(steps),
            duration_us=total_duration,
            duration_s=duration_s,
            peak_steps=AxisPeakSteps(
                peak_j1_steps=peak_steps[0],
                peak_j2_steps=peak_steps[1],
                peak_z_steps=peak_steps[2],
                peak_j4_steps=peak_steps[3],
            ),
            total_wire_bytes=len(raw_bytes),
        )
