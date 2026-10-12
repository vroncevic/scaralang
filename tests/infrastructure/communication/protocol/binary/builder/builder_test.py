# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
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
    Unit tests for BinaryFrameBuilder.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.protocol.binary_delimiter import BinaryDelimiter
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.infrastructure.communication.protocol.binary.builder.builder import BinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFrameBuilder(TestCase):
    '''
        Test cases verifying BinaryFrameBuilder frame assembling and serialization.

        It defines:

            :methods:
                | test_name - Verifies builder name identifier.
                | test_build_frame - Verifies generic frame construction and CRC.
                | test_build_joint_move - Verifies joint move frame encoding.
                | test_build_system_cmd - Verifies parameterless system command frames.
                | test_build_tool_cmd_pump - Verifies pump actuation frame encoding.
                | test_build_tool_cmd_valve - Verifies valve actuation frame encoding.
                | test_build_motor_config_cmd - Verifies motor configuration frame encoding.
                | test_build_wait_cmd - Verifies wait delay command frame encoding.
                | test_pack_frame - Verifies binary frame wire serialization.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with BinaryFrameBuilder instance.
        '''
        self.builder = BinaryFrameBuilder()

    def test_name(self) -> None:
        '''
            Tests builder name property returns expected identifier.
        '''
        self.assertEqual(self.builder.name, 'binary_frame_builder')

    def test_build_frame(self) -> None:
        '''
            Tests build_frame constructs BinaryFrame with correct fields.
        '''
        frame: BinaryFrame = self.builder.build_frame(
            msg_id=MessageId.CMD_PING, seq_num=10, payload=b'\x01\x02'
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_PING)
        self.assertEqual(frame.seq_num, 10)
        self.assertEqual(frame.payload, b'\x01\x02')
        self.assertGreater(frame.crc16, 0)

    def test_build_joint_move(self) -> None:
        '''
            Tests build_joint_move encodes JointSteps correctly.
        '''
        steps = JointSteps(
            target_j1_steps=100,
            target_j2_steps=200,
            target_z_steps=300,
            target_j4_steps=400,
            duration_us=1000,
            feedrate_scale=100
        )
        frame: BinaryFrame = self.builder.build_joint_move(seq_num=1, steps=steps)
        self.assertEqual(frame.msg_id, MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertEqual(frame.seq_num, 1)
        self.assertEqual(len(frame.payload), 22)

    def test_build_system_cmd(self) -> None:
        '''
            Tests build_system_cmd produces empty payload system frame.
        '''
        frame: BinaryFrame = self.builder.build_system_cmd(
            msg_id=MessageId.CMD_ESTOP, seq_num=5
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_ESTOP)
        self.assertEqual(frame.seq_num, 5)
        self.assertEqual(frame.payload, b'')

    def test_build_tool_cmd_pump(self) -> None:
        '''
            Tests build_tool_cmd for pump activation and deactivation.
        '''
        frame_on: BinaryFrame = self.builder.build_tool_cmd(
            seq_num=2, tool_id=ToolId.PUMP, state=True
        )
        self.assertEqual(frame_on.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(frame_on.payload, bytes([ToolId.PUMP, 1]))

        frame_off: BinaryFrame = self.builder.build_tool_cmd(
            seq_num=3, tool_id=ToolId.PUMP, state=False
        )
        self.assertEqual(frame_off.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(frame_off.payload, bytes([ToolId.PUMP, 0]))

    def test_build_tool_cmd_valve(self) -> None:
        '''
            Tests build_tool_cmd for valve actuation.
        '''
        frame: BinaryFrame = self.builder.build_tool_cmd(
            seq_num=4, tool_id=ToolId.VALVE, state=True
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(frame.payload, bytes([ToolId.VALVE, 1]))

    def test_build_motor_config_cmd(self) -> None:
        '''
            Tests build_motor_config_cmd produces motor configuration frame.
        '''
        frame: BinaryFrame = self.builder.build_motor_config_cmd(
            seq_num=7, mode=1, axis_mask=AxisMask.J1
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 7)
        self.assertEqual(frame.payload, bytes([1, AxisMask.J1]))

    def test_build_wait_cmd(self) -> None:
        '''
            Tests build_wait_cmd produces wait delay frame.
        '''
        frame: BinaryFrame = self.builder.build_wait_cmd(delay_ms=500, seq_num=8)
        self.assertEqual(frame.msg_id, MessageId.CMD_WAIT)
        self.assertEqual(frame.seq_num, 8)
        self.assertEqual(len(frame.payload), 4)

    def test_pack_frame(self) -> None:
        '''
            Tests pack_frame serializes frame with framing delimiters and CRC.
        '''
        frame: BinaryFrame = self.builder.build_system_cmd(
            msg_id=MessageId.CMD_PING, seq_num=1
        )
        packed: bytes = self.builder.pack_frame(frame=frame)
        self.assertEqual(packed[0], int(BinaryDelimiter.SOF1))
        self.assertEqual(packed[1], int(BinaryDelimiter.SOF2))
        self.assertEqual(packed[-1], int(BinaryDelimiter.EOF))
        self.assertEqual(len(packed), 2 + 3 + len(frame.payload) + 3)


if __name__ == '__main__':
    main()
