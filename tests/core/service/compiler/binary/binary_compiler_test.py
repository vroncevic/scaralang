# -*- coding: UTF-8 -*-

'''
Module
    binary_compiler_test.py
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
    Unit tests for BinaryCompiler class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.compiler.binary.binary_compiler import BinaryCompiler
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryCompiler(TestCase):
    '''
        Test cases verifying BinaryCompiler.

        It defines:

            :methods:
                | test_compile_plan - Verifies compiling trajectory plan into binary program.
    '''

    def setUp(self) -> None:
        '''Sets up compiler instance and mocks.'''
        self.mock_dispatcher = MagicMock()
        self.mock_metrics = MagicMock()
        self.compiler = BinaryCompiler(
            step_dispatcher=self.mock_dispatcher,
            metrics_calculator=self.mock_metrics,
        )

    def test_compile_plan(self) -> None:
        '''Verifies compile_plan delegates to dispatcher and metrics calculator.'''
        mock_plan = MagicMock()
        mock_plan.waypoints = ()
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=0,
            payload=b'\x00',
            crc16=0,
        )
        step = Step(
            frame=frame,
            raw_bytes=b'\x01\x02',
            duration_us=1500,
            target_steps=(10, 20, 30, 0),
            description='Test step',
            line_number=1,
        )
        expected_telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=1,
            duration_us=1500,
            duration_s=0.0015,
            peak_j1_steps=10,
            peak_j2_steps=20,
            peak_z_steps=30,
            peak_j4_steps=0,
            total_wire_bytes=2,
        )
        self.mock_dispatcher.dispatch_steps.return_value = (step,)
        self.mock_metrics.calculate_metrics.return_value = (
            1500,
            (10, 20, 30, 0),
        )
        self.mock_metrics.calculate_telemetry.return_value = expected_telemetry

        program: BinaryProgram = self.compiler.compile_plan(plan=mock_plan)
        self.assertEqual(program.total_duration_us, 1500)
        self.assertEqual(program.instruction_count, 1)
        self.assertEqual(program.raw_bytes, b'\x01\x02')
        self.assertEqual(program.step_counts, (10, 20, 30, 0))
        self.assertEqual(program.steps, (step,))
        self.assertEqual(program.telemetry, expected_telemetry)

    def test_protocol_conformance(self) -> None:
        '''Verifies BinaryCompiler satisfies IBinaryCompiler.'''
        self.assertIsInstance(self.compiler, IBinaryCompiler)


if __name__ == '__main__':
    main()
