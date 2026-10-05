# -*- coding: UTF-8 -*-

'''
Module
    program_test.py
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
    Unit tests for BinaryProgram model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryProgramTest(TestCase):
    '''Unit tests validating BinaryProgram purity, immutability, and attribute encapsulation.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify BinaryProgram fields.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0x1234,
        )
        step = Step(
            frame=frame,
            raw_bytes=b'\x01\x02',
            duration_us=1000,
            target_steps=(100, 200, 0, 0),
            description='Test step',
            line_number=1,
        )
        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=1,
            duration_us=1000,
            duration_s=0.001,
            total_wire_bytes=2,
        )
        program = BinaryProgram(
            steps=(step,),
            raw_bytes=b'\x01\x02',
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(100, 200, 0, 0),
            telemetry=telemetry,
        )
        self.assertEqual(len(program.steps), 1)
        self.assertEqual(program.steps[0], step)
        self.assertEqual(program.raw_bytes, b'\x01\x02')
        self.assertEqual(program.total_duration_us, 1000)
        self.assertEqual(program.instruction_count, 1)
        self.assertEqual(program.step_counts, (100, 200, 0, 0))
        self.assertEqual(program.telemetry, telemetry)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes raises FrozenInstanceError.'''
        telemetry = BinaryProgramTelemetry()
        program = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=telemetry,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(program, 'raw_bytes', b'test')


if __name__ == '__main__':
    main()
