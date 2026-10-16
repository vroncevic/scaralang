# -*- coding: UTF-8 -*-

'''
Module
    presenter_test.py
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

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.joint_step_coordinates import JointStepCoordinates
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.command.compile.inspection.framing.header.formatter import FrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.trailer.formatter import FrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.hex.formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.dependencies import DispatchDependencies
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.formatter import PayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.joint.formatter import JointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool.formatter import ToolCommandPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.presentation.step.dependencies import StepDependencies
from scaralang.infrastructure.command.compile.inspection.presentation.step.presenter import FrameStepPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.program.ipresenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.program.presenter import ProgramInspectionPresenter
from scaralang.infrastructure.protocol.binary.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.motion import BinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProgramInspectionPresenter(TestCase):
    '''Test suite verifying ProgramInspectionPresenter report generation.'''

    def setUp(self) -> None:
        '''Initializes presenter fixture.'''
        hex_fmt: HexStreamFormatter = HexStreamFormatter()
        dispatch_deps: DispatchDependencies = DispatchDependencies(
            joint_formatter=JointStepsPayloadFormatter(hex_formatter=hex_fmt),
            tool_formatter=ToolCommandPayloadFormatter(hex_formatter=hex_fmt),
            hex_formatter=hex_fmt,
            motion_unpacker=BinaryMotionPayloadUnpacker(),
            actuator_unpacker=BinaryActuatorPayloadUnpacker(),
        )
        step_deps: StepDependencies = StepDependencies(
            header_formatter=FrameHeaderFormatter(),
            payload_formatter=PayloadDispatcherFormatter(dependencies=dispatch_deps),
            trailer_formatter=FrameTrailerFormatter(),
            hex_formatter=hex_fmt,
        )
        step_presenter: FrameStepPresenter = FrameStepPresenter(
            dependencies=step_deps
        )
        self.presenter: ProgramInspectionPresenter = ProgramInspectionPresenter(
            step_presenter=step_presenter
        )

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.presenter, IProgramInspectionPresenter))
        self.assertFalse(isinstance(object(), IProgramInspectionPresenter))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        self.assertEqual(self.presenter.get_version(), '1.0.9')

    def test_present_empty_program(self) -> None:
        '''Verifies inspection presentation of empty binary program.'''
        empty_telemetry: BinaryProgramTelemetry = BinaryProgramTelemetry(
            source_instructions=0,
            compiled_steps=0,
            duration_us=0,
            duration_s=0.0,
            peak_steps=AxisPeakSteps(
                peak_j1_steps=0,
                peak_j2_steps=0,
                peak_z_steps=0,
                peak_j4_steps=0,
            ),
            total_wire_bytes=0,
        )
        program: BinaryProgram = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            telemetry=empty_telemetry,
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
        step: BinaryStep = BinaryStep(
            frame=frame,
            raw_bytes=b'\xAA\x55\x06\x01\x00\x56\x78\x0D',
            duration_us=10000,
            target_steps=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            description='HOME',
            line_number=2,
        )
        program: BinaryProgram = BinaryProgram(
            steps=(step,),
            raw_bytes=step.raw_bytes,
            total_duration_us=10000,
            instruction_count=1,
            step_counts=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=1,
                compiled_steps=1,
                duration_us=10000,
                duration_s=0.01,
                peak_steps=AxisPeakSteps(
                    peak_j1_steps=0,
                    peak_j2_steps=0,
                    peak_z_steps=0,
                    peak_j4_steps=0,
                ),
                total_wire_bytes=len(step.raw_bytes),
            ),
        )
        result: str = self.presenter.present_program(program=program)
        self.assertIn('SCARA BINARY FRAME INSPECTION: 1 Frames Compiled (8 bytes total)', result)
        self.assertIn('[Frame 0001] Step #1 | Line 2: HOME', result)


if __name__ == '__main__':
    main()
