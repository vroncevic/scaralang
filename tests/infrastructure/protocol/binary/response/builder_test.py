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
    Unit tests for BinaryResponseBuilder.
'''

from __future__ import annotations

from struct import unpack
from unittest import TestCase, main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.manipulator_status import ManipulatorStatus
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.move_event_type import MoveEventType
from scaralang.core.service.protocol.ibinary_response_builder import IBinaryResponseBuilder
from scaralang.infrastructure.protocol.binary.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.binary.builder.provides import BuilderProvides
from scaralang.infrastructure.protocol.binary.response.builder import BinaryResponseBuilder
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryResponseBuilder(TestCase):
    '''
        Unit test suite verifying BinaryResponseBuilder response frame packing.

        It defines:

            :methods:
                | setUp - Initializes builder collaborator before each test.
                | test_build_ack - Verifies ACK frame construction and payload.
                | test_build_nack - Verifies NACK frame construction and payload.
                | test_build_status - Verifies STATUS telemetry frame construction.
                | test_build_move_event - Verifies MOVE_EVENT frame construction.
                | test_structural_typing - Verifies instance satisfies IBinaryResponseBuilder.
                | test_get_version - Verifies version string retrieval.
    '''

    _builder: BinaryResponseBuilder

    def setUp(self) -> None:
        '''
            Sets up test fixture with BinaryResponseBuilder instance.
        '''
        builder_provides: BuilderProvides = BuilderFactory.create()
        self._builder = BinaryResponseBuilder(packer=builder_provides.packer)

    def test_build_ack(self) -> None:
        '''
            Verifies ACK frame fields and unpacked payload content.
        '''
        frame: BinaryFrame = self._builder.build_ack(
            cmd_id=MessageId.CMD_PING,
            seq_num=10,
            free_slots=5,
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_ACK)
        self.assertEqual(frame.seq_num, 10)
        unpacked = unpack(BinaryStructFormat.ACK, frame.payload)
        self.assertEqual(unpacked, (int(MessageId.CMD_PING), 5))

    def test_build_nack(self) -> None:
        '''
            Verifies NACK frame fields and unpacked payload content.
        '''
        frame: BinaryFrame = self._builder.build_nack(
            cmd_id=MessageId.CMD_PING,
            seq_num=11,
            error_code=3,
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_NACK)
        self.assertEqual(frame.seq_num, 11)
        unpacked = unpack(BinaryStructFormat.NACK, frame.payload)
        self.assertEqual(unpacked, (int(MessageId.CMD_PING), 3))

    def test_build_status(self) -> None:
        '''
            Verifies STATUS frame fields and telemetry values unpacking.

            :exceptions: None.
        '''
        status = ManipulatorStatus(
            system_state=1,
            is_busy=False,
            queue_count=3,
            j1_steps=1000,
            j2_steps=2000,
            z_steps=500,
            j4_steps=45,
        )
        frame: BinaryFrame = self._builder.build_status(
            seq_num=12,
            status=status,
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_STATUS)
        self.assertEqual(frame.seq_num, 12)
        unpacked = unpack(BinaryStructFormat.STATUS, frame.payload)
        self.assertEqual(unpacked, (1, 0, 3, 1000, 2000, 500, 45))

    def test_build_move_event(self) -> None:
        '''
            Verifies MOVE_EVENT frame fields and event code unpacking.
        '''
        frame: BinaryFrame = self._builder.build_move_event(
            seq_num=13,
            event_type=MoveEventType.DONE,
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertEqual(frame.seq_num, 13)
        unpacked = unpack(BinaryStructFormat.MOVE_EVENT, frame.payload)
        self.assertEqual(unpacked, (2, 13))

        raw_frame: BinaryFrame = self._builder.build_move_event(
            seq_num=14,
            event_type=1,
        )
        self.assertEqual(raw_frame.msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertEqual(raw_frame.seq_num, 14)
        raw_unpacked = unpack(BinaryStructFormat.MOVE_EVENT, raw_frame.payload)
        self.assertEqual(raw_unpacked, (1, 14))

    def test_structural_typing(self) -> None:
        '''
            Verifies BinaryResponseBuilder satisfies IBinaryResponseBuilder protocol.
        '''
        self.assertIsInstance(self._builder, IBinaryResponseBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.
        '''
        version: str = self._builder.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
