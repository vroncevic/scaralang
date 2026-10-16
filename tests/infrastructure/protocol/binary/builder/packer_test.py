# -*- coding: UTF-8 -*-

'''
Module
    packer_test.py
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
    Unit tests for BinaryFramePacker implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.protocol.binary.builder.packer import BinaryFramePacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFramePacker(TestCase):
    '''
        Test cases verifying BinaryFramePacker implementation.

        It defines:

            :methods:
                | test_build_frame - Verifies frame creation with correct attributes.
                | test_pack_frame - Verifies wire byte serialization and CRC.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_build_frame(self) -> None:
        '''
            Verifies frame construction with expected fields.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        frame: BinaryFrame = packer.build_frame(
            msg_id=MessageId.CMD_HOME,
            seq_num=10,
            payload=b'\x01\x02',
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_HOME)
        self.assertEqual(frame.seq_num, 10)
        self.assertEqual(frame.payload, b'\x01\x02')

    def test_pack_frame(self) -> None:
        '''
            Verifies packing a frame into wire bytes format with magic bytes.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        frame = packer.build_frame(msg_id=MessageId.CMD_HOME, seq_num=1)
        wire_bytes: bytes = packer.pack_frame(frame=frame)
        self.assertGreater(len(wire_bytes), 0)
        self.assertEqual(wire_bytes[0], 0xAA)
        self.assertEqual(wire_bytes[1], 0x55)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        version: str = packer.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
