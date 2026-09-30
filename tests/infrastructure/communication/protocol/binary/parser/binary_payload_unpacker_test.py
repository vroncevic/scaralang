# -*- coding: UTF-8 -*-

'''
Module
    binary_payload_unpacker_test.py
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
    Unit tests for BinaryPayloadUnpacker class.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryPayloadUnpacker(TestCase):
    '''
        Test cases verifying BinaryPayloadUnpacker methods.

        It defines:

            :methods:
                | test_name_property - Verifies name property.
                | test_unpack_joint_steps - Verifies unpack_joint_steps.
                | test_unpack_tool_cmd - Verifies unpack_tool_cmd.
                | test_unpack_ack - Verifies unpack_ack.
                | test_unpack_nack - Verifies unpack_nack.
                | test_unpack_motor_config - Verifies unpack_motor_config.
                | test_unpack_motor_config_partial - Verifies partial unpack_motor_config.
    '''

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns identifier string.
        '''
        unpacker = BinaryPayloadUnpacker()
        self.assertEqual(unpacker.name, 'binary_payload_unpacker')

    def test_unpack_joint_steps(self) -> None:
        '''
            Verifies unpacking joint steps payload.
        '''
        raw_steps = pack(str(BinaryStructFormat.JOINT_STEPS), 100, -200, 300, 400, 50000, 100)
        steps: JointSteps = BinaryPayloadUnpacker.unpack_joint_steps(raw_steps)
        self.assertEqual(steps.target_j1_steps, 100)
        self.assertEqual(steps.target_j2_steps, -200)
        self.assertEqual(steps.target_z_steps, 300)
        self.assertEqual(steps.target_j4_steps, 400)
        self.assertEqual(steps.duration_us, 50000)
        self.assertEqual(steps.feedrate_scale, 100)

    def test_unpack_tool_cmd(self) -> None:
        '''
            Verifies unpacking tool command payload.
        '''
        raw_tool = pack(str(BinaryStructFormat.TOOL_CMD), int(ToolId.VALVE), 1)
        tool_id, tool_state = BinaryPayloadUnpacker.unpack_tool_cmd(raw_tool)
        self.assertEqual(tool_id, int(ToolId.VALVE))
        self.assertTrue(tool_state)

    def test_unpack_ack(self) -> None:
        '''
            Verifies unpacking ACK payload.
        '''
        raw_ack = pack(str(BinaryStructFormat.ACK), int(MessageId.CMD_HOME), 7)
        ack_cmd, queue_space = BinaryPayloadUnpacker.unpack_ack(raw_ack)
        self.assertEqual(ack_cmd, int(MessageId.CMD_HOME))
        self.assertEqual(queue_space, 7)

    def test_unpack_nack(self) -> None:
        '''
            Verifies unpacking NACK payload.
        '''
        raw_nack = pack(str(BinaryStructFormat.NACK), int(MessageId.CMD_ENABLE), 3)
        nack_cmd, nack_reason = BinaryPayloadUnpacker.unpack_nack(raw_nack)
        self.assertEqual(nack_cmd, int(MessageId.CMD_ENABLE))
        self.assertEqual(nack_reason, 3)

    def test_unpack_motor_config(self) -> None:
        '''
            Verifies unpacking motor config payload.
        '''
        raw_motor = pack(str(BinaryStructFormat.CONFIG_MOTOR), 1, 0x0F)
        mode, axis_mask = BinaryPayloadUnpacker.unpack_motor_config(raw_motor)
        self.assertEqual(mode, 1)
        self.assertEqual(axis_mask, 0x0F)

    def test_unpack_motor_config_partial(self) -> None:
        '''
            Verifies unpacking motor config with single-byte and empty payloads.
        '''
        mode_single, axes_single = BinaryPayloadUnpacker.unpack_motor_config(b'\x02')
        self.assertEqual(mode_single, 2)
        self.assertEqual(axes_single, 0x0F)

        mode_empty, axes_empty = BinaryPayloadUnpacker.unpack_motor_config(b'')
        self.assertEqual(mode_empty, 0)
        self.assertEqual(axes_empty, 0x0F)


if __name__ == '__main__':
    main()
