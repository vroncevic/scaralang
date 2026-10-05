# -*- coding: UTF-8 -*-

'''
Module
    ibinary_payload_unpacker_test.py
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
    Unit tests for IBinaryPayloadUnpacker protocol compliance.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryPayloadUnpacker(TestCase):
    '''
        Test cases verifying IBinaryPayloadUnpacker structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies unpacker satisfies protocol.
                | test_name_property - Verifies name property returns expected identifier.
                | test_unpack_tool_cmd - Verifies tool command deserialization.
                | test_unpack_ack - Verifies ACK deserialization.
                | test_unpack_nack - Verifies NACK deserialization.
                | test_unpack_joint_steps - Verifies joint steps payload deserialization.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that factory creates an instance satisfying IBinaryPayloadUnpacker.
        '''
        unpacker = BinaryPayloadUnpackerFactory.create()
        self.assertIsInstance(unpacker, IBinaryPayloadUnpacker)

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns expected identifier.
        '''
        unpacker = BinaryPayloadUnpackerFactory.create()
        self.assertEqual(unpacker.name, 'binary_payload_unpacker')

    def test_unpack_tool_cmd(self) -> None:
        '''
            Verifies tool command payload unpacking through protocol contract.
        '''
        unpacker: IBinaryPayloadUnpacker = BinaryPayloadUnpackerFactory.create()
        raw_payload = pack(str(BinaryStructFormat.TOOL_CMD), 1, 1)
        tool_id, state = unpacker.unpack_tool_cmd(data=raw_payload)
        self.assertEqual(tool_id, 1)
        self.assertTrue(state)

    def test_unpack_ack(self) -> None:
        '''
            Verifies ACK payload unpacking through protocol contract.
        '''
        unpacker: IBinaryPayloadUnpacker = BinaryPayloadUnpackerFactory.create()
        raw_payload = pack(str(BinaryStructFormat.ACK), 10, 4)
        msg_id, queue_depth = unpacker.unpack_ack(data=raw_payload)
        self.assertEqual(msg_id, 10)
        self.assertEqual(queue_depth, 4)

    def test_unpack_nack(self) -> None:
        '''
            Verifies NACK payload unpacking through protocol contract.
        '''
        unpacker: IBinaryPayloadUnpacker = BinaryPayloadUnpackerFactory.create()
        raw_payload = pack(str(BinaryStructFormat.NACK), 20, 2)
        msg_id, error_code = unpacker.unpack_nack(data=raw_payload)
        self.assertEqual(msg_id, 20)
        self.assertEqual(error_code, 2)

    def test_unpack_joint_steps(self) -> None:
        '''
            Verifies joint steps payload unpacking through protocol contract.
        '''
        unpacker: IBinaryPayloadUnpacker = BinaryPayloadUnpackerFactory.create()
        raw_payload = pack(
            str(BinaryStructFormat.JOINT_STEPS),
            100, 200, 300, 400, 500, 600,
        )
        steps = unpacker.unpack_joint_steps(data=raw_payload)
        self.assertIsInstance(steps, JointSteps)
        self.assertEqual(steps.target_j1_steps, 100)
        self.assertEqual(steps.target_j2_steps, 200)
        self.assertEqual(steps.target_z_steps, 300)
        self.assertEqual(steps.target_j4_steps, 400)
        self.assertEqual(steps.duration_us, 500)
        self.assertEqual(steps.feedrate_scale, 600)

    def test_unpack_motor_config(self) -> None:
        '''
            Verifies motor config payload unpacking through protocol contract.
        '''
        unpacker: IBinaryPayloadUnpacker = BinaryPayloadUnpackerFactory.create()
        raw_payload = pack(str(BinaryStructFormat.CONFIG_MOTOR), 1, 0x0F)
        mode, axis_mask = unpacker.unpack_motor_config(data=raw_payload)
        self.assertEqual(mode, 1)
        self.assertEqual(axis_mask, 0x0F)


if __name__ == '__main__':
    main()
