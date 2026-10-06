# -*- coding: UTF-8 -*-

'''
Module
    program_inspection_presenter_test.py
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
    Unit tests for ProgramInspectionPresenter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.command.compile.inspection.presentation.frame_step_presenter_factory import FrameStepPresenterFactory
from scaralang.infrastructure.command.compile.inspection.presentation.iprogram_inspection_presenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.program_inspection_presenter import ProgramInspectionPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProgramInspectionPresenter(TestCase):
    '''Test suite verifying ProgramInspectionPresenter report generation.'''

    def setUp(self) -> None:
        '''Initializes presenter fixture.'''
        step_presenter_factory: FrameStepPresenterFactory = FrameStepPresenterFactory()
        self.presenter: ProgramInspectionPresenter = ProgramInspectionPresenter(
            step_presenter=step_presenter_factory.create()
        )

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.presenter, IProgramInspectionPresenter))
        self.assertFalse(isinstance(object(), IProgramInspectionPresenter))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        self.assertEqual(self.presenter.get_version(), '1.0.6')

    def test_present_empty_program(self) -> None:
        '''Verifies inspection presentation of empty binary program.'''
        program: BinaryProgram = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=BinaryProgramTelemetry(),
        )
        result: str = self.presenter.present_program(program=program)
        self.assertIn('SCARA BINARY FRAME INSPECTION: 0 Frames Compiled (0 bytes total)', result)
        self.assertIn('(No frames compiled)', result)

    def test_present_populated_program(self) -> None:
        '''Verifies inspection presentation of populated binary program.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
            payload=b'',
            crc16=0x5678,
        )
        step: Step = Step(
            frame=frame,
            raw_bytes=b'\xAA\x55\x06\x01\x00\x56\x78\x0D',
            duration_us=10000,
            target_steps=(0, 0, 0, 0),
            description='HOME',
            line_number=2,
        )
        program: BinaryProgram = BinaryProgram(
            steps=(step,),
            raw_bytes=step.raw_bytes,
            total_duration_us=10000,
            instruction_count=1,
            step_counts=(0, 0, 0, 0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=1,
                compiled_steps=1,
                duration_us=10000,
                duration_s=0.01,
                total_wire_bytes=len(step.raw_bytes),
            ),
        )
        result: str = self.presenter.present_program(program=program)
        self.assertIn('SCARA BINARY FRAME INSPECTION: 1 Frames Compiled (8 bytes total)', result)
        self.assertIn('[Frame 0001] Step #1 | Line 2: HOME', result)


if __name__ == '__main__':
    main()
