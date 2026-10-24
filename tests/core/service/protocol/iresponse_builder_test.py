# -*- coding: UTF-8 -*-

'''
Module
    iresponse_builder_test.py
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
    Unit tests for IBinaryResponseBuilder protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.status import ManipulatorStatus
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.protocol.event import MoveEventType
from scaralang.core.service.protocol.iresponse_builder import IBinaryResponseBuilder
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.response.dependencies import ResponseDependencies
from scaralang.infrastructure.protocol.response.factory import ResponseFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryResponseBuilder(TestCase):
    '''
        Test cases verifying IBinaryResponseBuilder structural subtyping.

        It defines:

            :methods:
                | setUp - Initializes response builder fixture satisfying protocol.
                | test_structural_compliance - Verifies builder satisfies protocol.
                | test_build_ack_and_nack - Verifies assembly of ACK and NACK frames.
                | test_build_status_and_move_event - Verifies assembly of STATUS and MOVE_EVENT.
                | test_get_version - Verifies semantic version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up response builder fixture through ResponseFactory.
        '''
        builder_provides = BuilderFactory.create()
        deps = ResponseDependencies(packer=builder_provides.packer)
        self.builder: IBinaryResponseBuilder = ResponseFactory.create(
            dependencies=deps
        ).builder

    def test_structural_compliance(self) -> None:
        '''
            Verifies instance satisfies IBinaryResponseBuilder structural protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.builder, IBinaryResponseBuilder)

    def test_build_ack_and_nack(self) -> None:
        '''
            Verifies building ACK and NACK response frames.

            :exceptions: None.
        '''
        ack_frame: BinaryFrame = self.builder.build_ack(
            cmd_id=MessageId.CMD_PING,
            seq_num=5,
            free_slots=8,
        )
        self.assertEqual(ack_frame.msg_id, MessageId.RESP_ACK)
        self.assertEqual(ack_frame.seq_num, 5)

        nack_frame: BinaryFrame = self.builder.build_nack(
            cmd_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=6,
            error_code=2,
        )
        self.assertEqual(nack_frame.msg_id, MessageId.RESP_NACK)
        self.assertEqual(nack_frame.seq_num, 6)

    def test_build_status_and_move_event(self) -> None:
        '''
            Verifies building STATUS and MOVE_EVENT response frames.

            :exceptions: None.
        '''
        status = ManipulatorStatus(
            system_state=0,
            is_busy=False,
            queue_count=2,
            j1_steps=100,
            j2_steps=200,
            z_steps=50,
            j4_steps=0,
        )
        status_frame: BinaryFrame = self.builder.build_status(
            seq_num=7,
            status=status,
        )
        self.assertEqual(status_frame.msg_id, MessageId.RESP_STATUS)
        self.assertEqual(status_frame.seq_num, 7)

        move_frame: BinaryFrame = self.builder.build_move_event(
            seq_num=8,
            event_type=MoveEventType.START,
        )
        self.assertEqual(move_frame.msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertEqual(move_frame.seq_num, 8)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns non-empty string.

            :exceptions: None.
        '''
        version: str = self.builder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
