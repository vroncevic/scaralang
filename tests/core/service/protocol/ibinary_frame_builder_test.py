# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_builder_test.py
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
    Unit tests for IBinaryFrameBuilder protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryFrameBuilder(TestCase):
    '''
        Test cases verifying IBinaryFrameBuilder structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies builder satisfies protocol.
                | test_name_property - Verifies name property returns expected identifier.
                | test_build_and_pack_frame - Verifies frame creation and byte serialization.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that factory creates an instance satisfying IBinaryFrameBuilder.
        '''
        builder = BinaryFrameBuilderFactory.create()
        self.assertIsInstance(builder, IBinaryFrameBuilder)

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns expected identifier.
        '''
        builder = BinaryFrameBuilderFactory.create()
        self.assertEqual(builder.name, 'binary_frame_builder')

    def test_build_and_pack_frame(self) -> None:
        '''
            Verifies frame construction and wire byte packing through protocol contract.
        '''
        builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        frame = builder.build_frame(msg_id=MessageId.CMD_HOME, seq_num=1)
        self.assertIsInstance(frame, BinaryFrame)
        self.assertEqual(frame.msg_id, MessageId.CMD_HOME)
        packed_bytes = builder.pack_frame(frame=frame)
        self.assertIsInstance(packed_bytes, bytes)
        self.assertTrue(len(packed_bytes) > 0)
        self.assertEqual(packed_bytes[0], 0xAA)
        self.assertEqual(packed_bytes[1], 0x55)

    def test_build_motor_config_cmd(self) -> None:
        '''
            Verifies motor configuration frame construction through protocol contract.
        '''
        builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        frame = builder.build_motor_config_cmd(seq_num=2, mode=1, axis_mask=0x0F)
        self.assertIsInstance(frame, BinaryFrame)
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 2)
        self.assertEqual(frame.payload, bytes([1, 0x0F]))

    def test_build_wait_cmd(self) -> None:
        '''
            Verifies wait command frame construction through protocol contract.
        '''
        builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        frame = builder.build_wait_cmd(delay_ms=250, seq_num=5)
        self.assertIsInstance(frame, BinaryFrame)
        self.assertEqual(frame.msg_id, MessageId.CMD_WAIT)
        self.assertEqual(frame.seq_num, 5)
        self.assertEqual(len(frame.payload), 4)


if __name__ == '__main__':
    main()
