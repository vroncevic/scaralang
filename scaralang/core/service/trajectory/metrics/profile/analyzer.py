# -*- coding: UTF-8 -*-

'''
Module
    analyzer.py
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

from typing import ClassVar

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.axis import AxisName
from scaralang.core.model.trajectory.metrics.peak import AxisPeakMetric

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AxisSpeedProfileAnalyzer:
    '''
        Profiles joint step execution to compute kinematic peak metrics per robot axis.

        It defines:

            :attributes:
                | NAME - Canonical component identifier name.
                | MICROSECONDS_PER_SECOND - Microseconds scaling factor per second.
                | MIN_DURATION_S - Minimal time quantum preventing division by zero.
                | ZERO_METRIC_FLOAT - Base floating point zero metric.
                | ZERO_METRIC_INT - Base integer zero metric.
                | _DEFAULT_AXES - Canonical sequence of manipulator AxisName enums.
                | name - Identifier name of the speed profile analyzer.
            :methods:
                | analyze_axis_peaks - Computes peak kinematic metrics across all 4 robot axes.
                | analyze_single_axis - Computes peak metrics for a specific joint axis.
    '''

    NAME: ClassVar[str] = 'axis_speed_profile_analyzer'
    MICROSECONDS_PER_SECOND: ClassVar[float] = 1_000_000.0
    MIN_DURATION_S: ClassVar[float] = 1e-6
    ZERO_METRIC_FLOAT: ClassVar[float] = 0.0
    ZERO_METRIC_INT: ClassVar[int] = 0

    _DEFAULT_AXES: ClassVar[tuple[AxisName, AxisName, AxisName, AxisName]] = (
        AxisName.J1,
        AxisName.J2,
        AxisName.Z,
        AxisName.J4,
    )

    @property
    def name(self) -> str:
        '''
            Gets the analyzer identifier name.

            :return: Analyzer name string.
        '''
        return self.NAME

    def analyze_single_axis(
        self,
        *,
        steps: tuple[BinaryStep, ...],
        axis_name: AxisName,
    ) -> AxisPeakMetric:
        '''
            Computes peak velocity, acceleration, and displacement for a single joint axis.

            :param steps: Sequence of compiled motion steps.
            :param axis_name: Identifier enum for the axis.
            :return: AxisPeakMetric containing observed peaks.
        '''
        if not steps:
            return AxisPeakMetric(
                axis_name=axis_name,
                peak_velocity=self.ZERO_METRIC_FLOAT,
                peak_acceleration=self.ZERO_METRIC_FLOAT,
                peak_steps=self.ZERO_METRIC_INT,
            )

        prev_coord: int = self.ZERO_METRIC_INT
        prev_velocity: float = self.ZERO_METRIC_FLOAT
        max_vel: float = self.ZERO_METRIC_FLOAT
        max_accel: float = self.ZERO_METRIC_FLOAT
        max_steps: int = self.ZERO_METRIC_INT

        for step in steps:
            coord: int

            match axis_name:
                case AxisName.J1:
                    coord = step.target_steps.j1
                case AxisName.J2:
                    coord = step.target_steps.j2
                case AxisName.Z:
                    coord = step.target_steps.z
                case AxisName.J4:
                    coord = step.target_steps.j4

            delta: int = abs(coord - prev_coord)

            if delta > max_steps:
                max_steps = delta

            duration_s: float = max(
                step.duration_us / self.MICROSECONDS_PER_SECOND,
                self.MIN_DURATION_S,
            )
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

    def analyze_axis_peaks(self, *, steps: tuple[BinaryStep, ...]) -> tuple[AxisPeakMetric, ...]:
        '''
            Analyzes joint step execution across all 4 axes to compute peak metrics.

            :param steps: Sequence of compiled binary motion steps.
            :return: Tuple of AxisPeakMetric for J1, J2, Z, and J4.
        '''
        results: list[AxisPeakMetric] = []

        for axis_name in self._DEFAULT_AXES:
            metric: AxisPeakMetric = self.analyze_single_axis(
                steps=steps,
                axis_name=axis_name,
            )
            results.append(metric)

        return tuple(results)
