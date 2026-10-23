# -*- coding: UTF-8 -*-

'''
Module
    actuator_test.py
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
    Unit tests for BinaryActuatorFrameBuilder implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
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


class TestBinaryActuatorFrameBuilder(TestCase):
    '''
        Test cases verifying BinaryActuatorFrameBuilder implementation.

        It defines:

            :methods:
                | test_build_tool_cmd - Verifies tool command frame construction.
                | test_build_motor_config_cmd - Verifies motor configuration frame construction.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_build_tool_cmd(self) -> None:
        '''
            Verifies tool command frame construction.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        actuator_builder = BinaryActuatorFrameBuilder(packer=packer)
        frame: BinaryFrame = actuator_builder.build_tool_cmd(
            tool_id=1,
            state=True,
            seq_num=3,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(frame.seq_num, 3)
        self.assertEqual(len(frame.payload), 2)

    def test_build_motor_config_cmd(self) -> None:
        '''
            Verifies motor configuration frame construction.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        actuator_builder = BinaryActuatorFrameBuilder(packer=packer)
        frame: BinaryFrame = actuator_builder.build_motor_config_cmd(
            seq_num=4,
            mode=2,
            axis_mask=0x03,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 4)
        self.assertEqual(frame.payload, bytes([2, 0x03]))

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        actuator_builder = BinaryActuatorFrameBuilder(packer=packer)
        version: str = actuator_builder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
