# -*- coding: UTF-8 -*-

'''
Module
    axis_speed_profile_analyzer_test.py
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

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric
from scaralang.core.service.trajectory.metrics.profile.axis_speed_profile_analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.profile.iaxis_speed_profile_analyzer import IAxisSpeedProfileAnalyzer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAxisSpeedProfileAnalyzer(TestCase):
    '''Test suite verifying AxisSpeedProfileAnalyzer performance calculations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        analyzer: AxisSpeedProfileAnalyzer = AxisSpeedProfileAnalyzer()
        self.assertTrue(isinstance(analyzer, IAxisSpeedProfileAnalyzer))

    def test_analyze_empty_steps(self) -> None:
        '''Verifies behavior when steps tuple is empty.'''
        analyzer: AxisSpeedProfileAnalyzer = AxisSpeedProfileAnalyzer()
        peaks: tuple[AxisPeakMetric, ...] = analyzer.analyze_axis_peaks(steps=())
        self.assertEqual(len(peaks), 4)
        for p in peaks:
            self.assertEqual(p.peak_velocity, 0.0)
            self.assertEqual(p.peak_acceleration, 0.0)
            self.assertEqual(p.peak_steps, 0)

    def test_analyze_axis_peaks(self) -> None:
        '''Verifies calculations of peak velocity, acceleration and step counts.'''
        analyzer: AxisSpeedProfileAnalyzer = AxisSpeedProfileAnalyzer()
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0,
        )
        # Step 1: 1000 steps on J1 in 100_000us (0.1s) -> vel = 10000 steps/s
        s1: Step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=100000,
            target_steps=(1000, 200, 50, 10),
            description='s1',
            line_number=1,
        )
        # Step 2: J1 reaches 3000 (+2000 steps) in 100_000us -> vel = 20000 steps/s
        s2: Step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=100000,
            target_steps=(3000, 400, 100, 20),
            description='s2',
            line_number=2,
        )
        peaks: tuple[AxisPeakMetric, ...] = analyzer.analyze_axis_peaks(steps=(s1, s2))
        self.assertEqual(len(peaks), 4)
        j1_metric: AxisPeakMetric = peaks[0]
        self.assertEqual(j1_metric.axis_name, 'J1')
        self.assertEqual(j1_metric.peak_steps, 2000)
        self.assertAlmostEqual(j1_metric.peak_velocity, 20000.0, places=2)
        self.assertTrue(j1_metric.peak_acceleration > 0.0)


if __name__ == '__main__':
    main()
