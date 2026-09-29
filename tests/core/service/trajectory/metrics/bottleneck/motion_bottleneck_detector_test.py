# -*- coding: UTF-8 -*-

'''
Module
    motion_bottleneck_detector_test.py
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
    Unit tests for MotionBottleneckDetector service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.trajectory.bottleneck_incident import BottleneckIncident
from scaralang.core.service.trajectory.metrics.bottleneck.imotion_bottleneck_detector import IMotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.bottleneck.motion_bottleneck_detector import MotionBottleneckDetector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionBottleneckDetector(TestCase):
    '''Test suite verifying MotionBottleneckDetector incident detection.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        detector: MotionBottleneckDetector = MotionBottleneckDetector()
        self.assertTrue(isinstance(detector, IMotionBottleneckDetector))

    def test_detect_empty_steps(self) -> None:
        '''Verifies behavior with empty step sequence.'''
        detector: MotionBottleneckDetector = MotionBottleneckDetector()
        incidents: tuple[BottleneckIncident, ...] = detector.detect_bottlenecks(steps=())
        self.assertEqual(len(incidents), 0)

    def test_detect_step_bottleneck_no_motion(self) -> None:
        '''Verifies None returned when step has zero displacement.'''
        detector: MotionBottleneckDetector = MotionBottleneckDetector()
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0,
        )
        step: Step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=10000,
            target_steps=(0, 0, 0, 0),
            description='idle',
            line_number=1,
        )
        incident: BottleneckIncident | None = detector.detect_step_bottleneck(
            step=step,
            step_index=0,
            prev_coords=(0, 0, 0, 0),
        )
        self.assertIsNone(incident)

    def test_detect_bottlenecks_identifies_limiting_axes(self) -> None:
        '''Verifies limiting axes and constraint categories are accurately detected.'''
        detector: MotionBottleneckDetector = MotionBottleneckDetector()
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0,
        )
        # Step 0: J1 moves 5000 steps, Z moves 100 -> J1 limiting, duration 50000us (VELOCITY)
        s1: Step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=50000,
            target_steps=(5000, 50, 100, 10),
            description='s1',
            line_number=1,
        )
        # Step 1: Z moves from 100 to 2000 (delta 1900), others unchanged -> Z limiting
        s2: Step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=5000,
            target_steps=(5000, 50, 2000, 10),
            description='s2',
            line_number=2,
        )
        incidents: tuple[BottleneckIncident, ...] = detector.detect_bottlenecks(steps=(s1, s2))
        self.assertEqual(len(incidents), 2)
        self.assertEqual(incidents[0].limiting_axis, 'J1')
        self.assertEqual(incidents[0].constraint_type, 'VELOCITY')
        self.assertEqual(incidents[1].limiting_axis, 'Z')
        self.assertEqual(incidents[1].constraint_type, 'ACCELERATION')


if __name__ == '__main__':
    main()
