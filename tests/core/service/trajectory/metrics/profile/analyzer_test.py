# -*- coding: UTF-8 -*-

'''
Module
    analyzer_test.py
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
    Unit tests for AxisSpeedProfileAnalyzer service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.axis import AxisName
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.trajectory.metrics.peak import AxisPeakMetric
from scaralang.core.service.trajectory.metrics.profile.analyzer import AxisSpeedProfileAnalyzer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAxisSpeedProfileAnalyzer(TestCase):
    '''Test suite verifying AxisSpeedProfileAnalyzer kinematic profiling calculations.'''

    def test_name_property(self) -> None:
        '''Verifies name property returns correct identifier string.'''
        speed_analyzer = AxisSpeedProfileAnalyzer()
        self.assertEqual(speed_analyzer.name, 'axis_speed_profile_analyzer')

    def test_analyze_empty_step_sequence(self) -> None:
        '''Verifies behavior when analyzing empty step sequence.'''
        speed_analyzer = AxisSpeedProfileAnalyzer()
        peak_results = speed_analyzer.analyze_axis_peaks(steps=())
        self.assertEqual(len(peak_results), 4)
        for metric in peak_results:
            self.assertEqual(metric.peak_velocity, 0.0)
            self.assertEqual(metric.peak_acceleration, 0.0)
            self.assertEqual(metric.peak_steps, 0)

    def test_analyze_axis_peaks_calculation(self) -> None:
        '''Verifies calculation of maximum velocity, acceleration and microstep counts.'''
        speed_analyzer = AxisSpeedProfileAnalyzer()
        dummy_frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0,
        )
        step_one = BinaryStep(
            frame=dummy_frame,
            raw_bytes=b'',
            duration_us=100000,
            target_steps=JointStepCoordinates(j1=1000, j2=200, z=50, j4=10),
            description='s1',
            line_number=1,
        )
        step_two = BinaryStep(
            frame=dummy_frame,
            raw_bytes=b'',
            duration_us=100000,
            target_steps=JointStepCoordinates(j1=3000, j2=400, z=100, j4=20),
            description='s2',
            line_number=2,
        )
        peaks: tuple[AxisPeakMetric, ...] = speed_analyzer.analyze_axis_peaks(
            steps=(step_one, step_two)
        )
        self.assertEqual(len(peaks), 4)
        j1_peak = peaks[0]
        self.assertEqual(j1_peak.axis_name, AxisName.J1)
        self.assertEqual(j1_peak.peak_steps, 2000)
        self.assertAlmostEqual(j1_peak.peak_velocity, 20000.0, places=2)
        self.assertTrue(j1_peak.peak_acceleration > 0.0)


if __name__ == '__main__':
    main()
