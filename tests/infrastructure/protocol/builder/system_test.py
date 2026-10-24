# -*- coding: UTF-8 -*-

'''
Module
    system_test.py
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
    Unit tests for BinarySystemFrameBuilder implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.infrastructure.protocol.builder.packer import BinaryFramePacker
from scaralang.infrastructure.protocol.builder.system import BinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinarySystemFrameBuilder(TestCase):
    '''
        Test cases verifying BinarySystemFrameBuilder implementation.

        It defines:

            :methods:
                | test_build_system_and_wait_cmd - Verifies system and wait frame creation.
                | test_build_jog_and_override_frame - Verifies jog and override frame creation.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_build_system_and_wait_cmd(self) -> None:
        '''
            Verifies system and wait frame creation.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        system_builder = BinarySystemFrameBuilder(packer=packer)

        sys_frame: BinaryFrame = system_builder.build_system_cmd(
            msg_id=MessageId.CMD_ESTOP,
            seq_num=1,
        )
        self.assertEqual(sys_frame.msg_id, MessageId.CMD_ESTOP)
        self.assertEqual(sys_frame.seq_num, 1)

        wait_frame: BinaryFrame = system_builder.build_wait_cmd(
            delay_ms=250,
            seq_num=2,
        )
        self.assertEqual(wait_frame.msg_id, MessageId.CMD_WAIT)
        self.assertEqual(wait_frame.seq_num, 2)
        self.assertEqual(len(wait_frame.payload), 4)

    def test_build_jog_and_override_frame(self) -> None:
        '''
            Verifies jog and override frame creation.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        system_builder = BinarySystemFrameBuilder(packer=packer)

        jog_frame: BinaryFrame = system_builder.build_jog_frame(
            joint_id=1,
            step=-50,
            seq_num=3,
        )
        self.assertEqual(jog_frame.msg_id, MessageId.CMD_JOG_JOINT)
        self.assertEqual(jog_frame.seq_num, 3)

        override_frame: BinaryFrame = system_builder.build_override_frame(
            pct=90,
            seq_num=4,
        )
        self.assertEqual(override_frame.msg_id, MessageId.CMD_OVERRIDE)
        self.assertEqual(override_frame.seq_num, 4)
        self.assertEqual(override_frame.payload, bytes([90]))

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        system_builder = BinarySystemFrameBuilder(packer=packer)
        version: str = system_builder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
