# -*- coding: UTF-8 -*-

'''
Module
    iactuator_builder_test.py
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
    Unit tests for IBinaryActuatorFrameBuilder protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.infrastructure.protocol.builder.actuator import BinaryActuatorFrameBuilder
from scaralang.infrastructure.protocol.builder.packer import BinaryFramePacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryActuatorFrameBuilder(TestCase):
    '''
        Test cases verifying IBinaryActuatorFrameBuilder structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies builder satisfies protocol.
                | test_build_tool_cmd - Verifies tool command frame construction.
                | test_build_motor_config_cmd - Verifies motor configuration frame construction.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete builder satisfies IBinaryActuatorFrameBuilder.

            :exceptions: None.
        '''
        builder = BinaryActuatorFrameBuilder(packer=BinaryFramePacker())
        self.assertIsInstance(builder, IBinaryActuatorFrameBuilder)
        self.assertFalse(isinstance(object(), IBinaryActuatorFrameBuilder))

    def test_build_tool_cmd(self) -> None:
        '''
            Verifies tool command frame construction through protocol contract.

            :exceptions: None.
        '''
        builder = BinaryActuatorFrameBuilder(packer=BinaryFramePacker())
        frame = builder.build_tool_cmd(
            tool_id=0,
            state=True,
            seq_num=3,
        )
        self.assertIsInstance(frame, BinaryFrame)
        self.assertEqual(frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(frame.seq_num, 3)

    def test_build_motor_config_cmd(self) -> None:
        '''
            Verifies motor config frame construction through protocol contract.

            :exceptions: None.
        '''
        builder = BinaryActuatorFrameBuilder(packer=BinaryFramePacker())
        frame = builder.build_motor_config_cmd(seq_num=4, mode=1, axis_mask=0x0F)
        self.assertIsInstance(frame, BinaryFrame)
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 4)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        builder = BinaryActuatorFrameBuilder(packer=BinaryFramePacker())
        version: str = builder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
