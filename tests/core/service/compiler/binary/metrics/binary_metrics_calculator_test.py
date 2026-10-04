# -*- coding: UTF-8 -*-

'''
Module
    binary_metrics_calculator_test.py
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
    Unit tests for BinaryMetricsCalculator class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.compiler.binary.metrics.binary_metrics_calculator import BinaryMetricsCalculator
from scaralang.core.service.compiler.binary.metrics.ibinary_metrics_calculator import IBinaryMetricsCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryMetricsCalculator(TestCase):
    '''
        Test cases verifying BinaryMetricsCalculator.

        It defines:

            :methods:
                | test_calculate_metrics_empty - Verifies calculation with zero steps.
                | test_calculate_metrics_populated - Verifies calculation with populated steps.
    '''

    def setUp(self) -> None:
        '''Sets up calculator instance.'''
        self.calculator = BinaryMetricsCalculator()

    def test_calculate_metrics_empty(self) -> None:
        '''Verifies calculation on empty steps list.'''
        total_duration, peak_steps = self.calculator.calculate_metrics(steps=())
        self.assertEqual(total_duration, 0)
        self.assertEqual(peak_steps, (0, 0, 0, 0))

    def test_calculate_metrics_populated(self) -> None:
        '''Verifies calculation on populated steps list.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=0,
            payload=b'',
            crc16=0,
        )
        step1 = Step(
            frame=frame,
            target_steps=(100, -200, 50, 10),
            duration_us=1000,
            raw_bytes=b'',
            description='Step 1',
            line_number=1,
        )
        step2 = Step(
            frame=frame,
            target_steps=(-150, 100, 300, -20),
            duration_us=2500,
            raw_bytes=b'',
            description='Step 2',
            line_number=2,
        )
        total_duration, peak_steps = self.calculator.calculate_metrics(
            steps=(step1, step2)
        )
        self.assertEqual(total_duration, 3500)
        self.assertEqual(peak_steps, (150, 200, 300, 20))

    def test_calculate_telemetry(self) -> None:
        '''Verifies calculate_telemetry returns populated BinaryProgramTelemetry.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0x1234,
        )
        step = Step(
            frame=frame,
            target_steps=(100, -200, 50, 10),
            duration_us=1000,
            raw_bytes=b'\x01\x02',
            description='Step 1',
            line_number=1,
        )
        telemetry = self.calculator.calculate_telemetry(
            steps=(step,), raw_bytes=b'\x01\x02'
        )
        self.assertEqual(telemetry.source_instructions, 1)
        self.assertEqual(telemetry.compiled_steps, 1)
        self.assertEqual(telemetry.duration_us, 1000)
        self.assertAlmostEqual(telemetry.duration_s, 0.001)
        self.assertEqual(telemetry.peak_steps.peak_j1_steps, 100)
        self.assertEqual(telemetry.peak_steps.peak_j2_steps, 200)
        self.assertEqual(telemetry.peak_steps.peak_z_steps, 50)
        self.assertEqual(telemetry.peak_steps.peak_j4_steps, 10)
        self.assertEqual(telemetry.total_wire_bytes, 2)

    def test_protocol_conformance(self) -> None:
        '''Verifies BinaryMetricsCalculator satisfies IBinaryMetricsCalculator.'''
        self.assertIsInstance(self.calculator, IBinaryMetricsCalculator)


if __name__ == '__main__':
    main()
