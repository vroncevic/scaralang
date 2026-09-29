# -*- coding: UTF-8 -*-

'''
Module
    frame_step_presenter_test.py
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
    Unit tests for FrameStepPresenter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.command.compile.inspection.framing.frame_header_formatter import FrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.frame_trailer_formatter import FrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.joint_steps_payload_formatter import JointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.payload_dispatcher_formatter import PayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool_command_payload_formatter import ToolCommandPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.presentation.frame_step_presenter import FrameStepPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.iframe_step_presenter import IFrameStepPresenter
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameStepPresenter(TestCase):
    '''Test suite verifying FrameStepPresenter step card rendering.'''

    def setUp(self) -> None:
        '''Initializes presenter with collaborating formatters.'''
        hex_fmt: HexStreamFormatter = HexStreamFormatter()
        self.presenter: FrameStepPresenter = FrameStepPresenter(
            header_formatter=FrameHeaderFormatter(),
            payload_formatter=PayloadDispatcherFormatter(
                joint_formatter=JointStepsPayloadFormatter(hex_formatter=hex_fmt),
                tool_formatter=ToolCommandPayloadFormatter(hex_formatter=hex_fmt),
                hex_formatter=hex_fmt,
                unpacker=BinaryPayloadUnpacker(),
            ),
            trailer_formatter=FrameTrailerFormatter(),
            hex_formatter=hex_fmt,
        )

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.presenter, IFrameStepPresenter))

    def test_present_step(self) -> None:
        '''Verifies visual card formatting for a compiled step.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
            payload=b'',
            crc16=0x1234,
        )
        step: Step = Step(
            frame=frame,
            raw_bytes=b'\xAA\x55\x06\x01\x00\x12\x34\x0D',
            duration_us=10000,
            target_steps=(0, 0, 0, 0),
            description='HOME',
            line_number=4,
        )
        result: str = self.presenter.present_step(step=step, index=1)
        self.assertIn('[Frame 0001] Step #1 | Line 4: HOME', result)
        self.assertIn('SOF=[AA 55]', result)
        self.assertIn('MSG=0x06 (CMD_HOME)', result)
        self.assertIn('CRC16=0x1234', result)
        self.assertIn('Wire Frame:', result)


if __name__ == '__main__':
    main()
