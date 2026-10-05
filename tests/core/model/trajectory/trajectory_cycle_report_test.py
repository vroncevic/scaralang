# -*- coding: UTF-8 -*-

'''
Module
    trajectory_cycle_report_test.py
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
    Unit tests for TrajectoryCycleReport data model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric
from scaralang.core.model.trajectory.bottleneck_incident import BottleneckIncident
from scaralang.core.model.trajectory.trajectory_cycle_report import TrajectoryCycleReport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCycleReportTest(TestCase):
    '''Unit tests validating TrajectoryCycleReport aggregate dataclass.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify correct field assignment upon instantiation.'''
        peak = AxisPeakMetric(
            axis_name='J1',
            peak_velocity=2.5,
            peak_acceleration=10.0,
            peak_steps=1200
        )
        bottleneck = BottleneckIncident(
            step_index=1,
            limiting_axis='J1',
            constraint_type='VELOCITY',
            duration_us=150000
        )
        report = TrajectoryCycleReport(
            total_duration_us=150000,
            total_distance_mm=125.5,
            axis_peaks=(peak,),
            bottlenecks=(bottleneck,)
        )
        self.assertEqual(report.total_duration_us, 150000)
        self.assertEqual(report.total_distance_mm, 125.5)
        self.assertEqual(len(report.axis_peaks), 1)
        self.assertEqual(len(report.bottlenecks), 1)

    def test_immutability(self) -> None:
        '''Verify that attributes cannot be modified on frozen dataclass.'''
        report = TrajectoryCycleReport(
            total_duration_us=100,
            total_distance_mm=10.0,
            axis_peaks=(),
            bottlenecks=()
        )
        with self.assertRaises(AttributeError):
            report.total_duration_us = 200  # type: ignore[misc]


if __name__ == '__main__':
    main()
