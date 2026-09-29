# -*- coding: UTF-8 -*-

'''
Module
    trajectory_cycle_report.py
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
    Defines immutable TrajectoryCycleReport model aggregating timing and kinematic performance metrics.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric
from scaralang.core.model.trajectory.bottleneck_incident import BottleneckIncident

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class TrajectoryCycleReport:
    '''
        Comprehensive cycle-time and performance telemetry report for a compiled trajectory.

        It defines:

            :attributes:
                | total_duration_us - Total trajectory execution duration in microseconds.
                | total_distance_mm - Cumulative Cartesian 3D path distance in millimeters.
                | axis_peaks - Tuple of peak kinematic measurements per axis.
                | bottlenecks - Tuple of recorded speed/acceleration bottlenecks.
    '''

    total_duration_us: int
    total_distance_mm: float
    axis_peaks: tuple[AxisPeakMetric, ...]
    bottlenecks: tuple[BottleneckIncident, ...]
