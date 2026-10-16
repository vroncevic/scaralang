# -*- coding: UTF-8 -*-

'''
Module
    motion_test.py
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
    Unit tests for BinaryMotionFrameBuilder implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.protocol.binary.builder.motion import BinaryMotionFrameBuilder
from scaralang.infrastructure.protocol.binary.builder.packer import BinaryFramePacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryMotionFrameBuilder(TestCase):
    '''
        Test cases verifying BinaryMotionFrameBuilder implementation.

        It defines:

            :methods:
                | test_build_joint_move - Verifies joint move frame construction.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_build_joint_move(self) -> None:
        '''
            Verifies joint move binary frame construction with packed payload.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        motion_builder = BinaryMotionFrameBuilder(packer=packer)
        steps = JointSteps(
            target_j1_steps=100,
            target_j2_steps=200,
            target_z_steps=300,
            target_j4_steps=400,
            duration_us=1000,
            feedrate_scale=100,
        )
        frame: BinaryFrame = motion_builder.build_joint_move(
            steps=steps,
            seq_num=7,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertEqual(frame.seq_num, 7)
        self.assertGreater(len(frame.payload), 0)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        motion_builder = BinaryMotionFrameBuilder(packer=packer)
        version: str = motion_builder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
