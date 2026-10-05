# -*- coding: UTF-8 -*-

'''
Module
    axis_speed_profile_analyzer.py
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
    Defines AxisSpeedProfileAnalyzer analyzing joint velocity, acceleration, and step peaks.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AxisSpeedProfileAnalyzer:
    '''
        Profiles joint step execution to compute kinematic peak metrics per robot axis.

        It defines:

            :attributes:
                | name - Identifier name of the speed profile analyzer.
            :methods:
                | analyze_axis_peaks - Computes peak kinematic metrics across all 4 robot axes.
                | analyze_single_axis - Computes peak metrics for a specific joint axis index.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the analyzer identifier name.

            :return: Analyzer name string.
        '''
        return 'axis_speed_profile_analyzer'

    def analyze_single_axis(
        self,
        *,
        steps: tuple[Step, ...],
        axis_index: int,
        axis_name: str
    ) -> AxisPeakMetric:
        '''
            Computes peak velocity, acceleration, and displacement for a single joint axis.

            :param steps: Sequence of compiled motion steps.
            :param axis_index: Coordinate index in target_steps (0=J1, 1=J2, 2=Z, 3=J4).
            :param axis_name: Identifier name for the axis.
            :return: AxisPeakMetric containing observed peaks.
        '''
        if not steps:
            return AxisPeakMetric(
                axis_name=axis_name,
                peak_velocity=0.0,
                peak_acceleration=0.0,
                peak_steps=0,
            )

        prev_coord: int = 0
        prev_velocity: float = 0.0
        max_vel: float = 0.0
        max_accel: float = 0.0
        max_steps: int = 0

        for step in steps:
            coord: int = step.target_steps[axis_index]
            delta: int = abs(coord - prev_coord)

            if delta > max_steps:
                max_steps = delta

            duration_s: float = max(step.duration_us / 1000000.0, 0.000001)
            vel: float = float(delta) / duration_s

            if vel > max_vel:
                max_vel = vel

            accel: float = abs(vel - prev_velocity) / duration_s

            if accel > max_accel:
                max_accel = accel

            prev_coord = coord
            prev_velocity = vel

        return AxisPeakMetric(
            axis_name=axis_name,
            peak_velocity=max_vel,
            peak_acceleration=max_accel,
            peak_steps=max_steps,
        )

    def analyze_axis_peaks(self, *, steps: tuple[Step, ...]) -> tuple[AxisPeakMetric, ...]:
        '''
            Analyzes joint step execution across all 4 axes to compute peak metrics.

            :param steps: Sequence of compiled binary motion steps.
            :return: Tuple of AxisPeakMetric for J1, J2, Z, and J4.
        '''
        axes: tuple[tuple[int, str], ...] = (
            (0, 'J1'),
            (1, 'J2'),
            (2, 'Z'),
            (3, 'J4'),
        )
        results: list[AxisPeakMetric] = []

        for index, name in axes:
            metric: AxisPeakMetric = self.analyze_single_axis(
                steps=steps,
                axis_index=index,
                axis_name=name,
            )
            results.append(metric)

        return tuple(results)
