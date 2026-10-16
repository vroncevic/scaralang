# -*- coding: UTF-8 -*-

'''
Module
    ibinary_system_frame_builder_test.py
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
    Unit tests for IBinarySystemFrameBuilder protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_system_frame_builder import IBinarySystemFrameBuilder
from scaralang.infrastructure.protocol.binary.builder.packer import BinaryFramePacker
from scaralang.infrastructure.protocol.binary.builder.system import BinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinarySystemFrameBuilder(TestCase):
    '''
        Test cases verifying IBinarySystemFrameBuilder structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies builder satisfies protocol.
                | test_build_system_and_wait_cmd - Verifies system and wait frame creation.
                | test_build_jog_and_override_frame - Verifies jog and override frame creation.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete builder satisfies IBinarySystemFrameBuilder.

            :exceptions: None.
        '''
        builder = BinarySystemFrameBuilder(packer=BinaryFramePacker())
        self.assertIsInstance(builder, IBinarySystemFrameBuilder)
        self.assertFalse(isinstance(object(), IBinarySystemFrameBuilder))

    def test_build_system_and_wait_cmd(self) -> None:
        '''
            Verifies system and wait frame creation through protocol contract.

            :exceptions: None.
        '''
        builder = BinarySystemFrameBuilder(packer=BinaryFramePacker())
        sys_frame = builder.build_system_cmd(msg_id=MessageId.CMD_HOME, seq_num=1)
        self.assertIsInstance(sys_frame, BinaryFrame)
        self.assertEqual(sys_frame.msg_id, MessageId.CMD_HOME)

        wait_frame = builder.build_wait_cmd(delay_ms=500, seq_num=2)
        self.assertIsInstance(wait_frame, BinaryFrame)
        self.assertEqual(wait_frame.msg_id, MessageId.CMD_WAIT)

    def test_build_jog_and_override_frame(self) -> None:
        '''
            Verifies jog and override frame creation through protocol contract.

            :exceptions: None.
        '''
        builder = BinarySystemFrameBuilder(packer=BinaryFramePacker())
        jog_frame = builder.build_jog_frame(joint_id=0, step=100, seq_num=3)
        self.assertIsInstance(jog_frame, BinaryFrame)
        self.assertEqual(jog_frame.msg_id, MessageId.CMD_JOG_JOINT)

        override_frame = builder.build_override_frame(pct=80, seq_num=4)
        self.assertIsInstance(override_frame, BinaryFrame)
        self.assertEqual(override_frame.msg_id, MessageId.CMD_OVERRIDE)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        builder = BinarySystemFrameBuilder(packer=BinaryFramePacker())
        version: str = builder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
