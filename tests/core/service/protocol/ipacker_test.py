# -*- coding: UTF-8 -*-

'''
Module
    ipacker_test.py
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
    Unit tests for IBinaryFramePacker protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.infrastructure.protocol.builder.packer import BinaryFramePacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryFramePacker(TestCase):
    '''
        Test cases verifying IBinaryFramePacker structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies packer satisfies protocol.
                | test_build_and_pack_frame - Verifies frame creation and byte serialization.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete packer satisfies IBinaryFramePacker.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        self.assertIsInstance(packer, IBinaryFramePacker)
        self.assertFalse(isinstance(object(), IBinaryFramePacker))

    def test_build_and_pack_frame(self) -> None:
        '''
            Verifies frame construction and wire byte packing through protocol contract.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        frame = packer.build_frame(msg_id=MessageId.CMD_HOME, seq_num=1)
        self.assertIsInstance(frame, BinaryFrame)
        self.assertEqual(frame.msg_id, MessageId.CMD_HOME)
        packed_bytes = packer.pack_frame(frame=frame)
        self.assertIsInstance(packed_bytes, bytes)
        self.assertTrue(len(packed_bytes) > 0)
        self.assertEqual(packed_bytes[0], 0xAA)
        self.assertEqual(packed_bytes[1], 0x55)

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
