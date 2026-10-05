# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_test.py
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
    Unit tests for BinaryFrame protocol domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameTest(TestCase):
    '''Unit tests validating BinaryFrame purity, immutability, and attribute values.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper initialization and access of BinaryFrame fields.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=42,
            payload=b'\x01\x02\x03\x04',
            crc16=0xABCD,
        )
        self.assertIs(frame.msg_id, MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertEqual(frame.seq_num, 42)
        self.assertEqual(frame.payload, b'\x01\x02\x03\x04')
        self.assertEqual(frame.crc16, 0xABCD)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes on BinaryFrame raises FrozenInstanceError.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
            payload=b'',
            crc16=0x1234,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(frame, 'seq_num', 2)

    def test_equality(self) -> None:
        '''Verify that two BinaryFrame instances with identical fields evaluate equal.'''
        frame_a = BinaryFrame(
            msg_id=MessageId.CMD_ENABLE,
            seq_num=10,
            payload=b'\x00',
            crc16=0x5678,
        )
        frame_b = BinaryFrame(
            msg_id=MessageId.CMD_ENABLE,
            seq_num=10,
            payload=b'\x00',
            crc16=0x5678,
        )
        self.assertEqual(frame_a, frame_b)


if __name__ == '__main__':
    main()
