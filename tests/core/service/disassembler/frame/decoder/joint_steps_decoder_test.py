# -*- coding: UTF-8 -*-

'''
Module
    joint_steps_decoder_test.py
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
    Unit tests for JointStepsDecoder component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.disassembler.frame.decoder.idecoder import IFramePayloadDecoder
from scaralang.core.service.disassembler.frame.decoder.joint_steps_decoder import JointStepsDecoder
from scaralang.infrastructure.protocol.binary.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.binary.parser.unpacker.motion import BinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointStepsDecoder(TestCase):
    '''
    Test cases verifying JointStepsDecoder operations.

    It defines:

        :methods:
            | setUp - Sets up decoder fixture.
            | test_protocol_conformance - Verifies protocol check.
            | test_can_decode - Verifies message ID matching.
            | test_decode - Verifies formatting joint steps payload.
            | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
        Sets up decoder with concrete unpacker fixture.
        '''
        self.unpacker: BinaryMotionPayloadUnpacker = (
            BinaryMotionPayloadUnpacker()
        )
        self.decoder: JointStepsDecoder = JointStepsDecoder(
            unpacker=self.unpacker
        )

    def test_protocol_conformance(self) -> None:
        '''
        Verifies decoder satisfies IFramePayloadDecoder protocol.
        '''
        self.assertIsInstance(self.decoder, IFramePayloadDecoder)

    def test_can_decode(self) -> None:
        '''
        Verifies can_decode matches only CMD_MOVE_JOINT_STEPS.
        '''
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_MOVE_JOINT_STEPS)))
        self.assertFalse(self.decoder.can_decode(msg_id=int(MessageId.CMD_HOME)))

    def test_decode(self) -> None:
        '''
        Verifies decode parses joint steps payload accurately.
        '''
        motion_builder = BuilderFactory.create().motion
        frame: BinaryFrame = motion_builder.build_joint_move(
            steps=JointSteps(
                target_j1_steps=100,
                target_j2_steps=200,
                target_z_steps=300,
                target_j4_steps=400,
                duration_us=50000,
                feedrate_scale=100,
            ),
            seq_num=1,
        )
        detail: str = self.decoder.decode(frame=frame)
        self.assertIn('J1=100', detail)
        self.assertIn('J2=200', detail)
        self.assertIn('Z=300', detail)
        self.assertIn('J4=400', detail)
        self.assertIn('dur=50000us', detail)

    def test_get_version(self) -> None:
        '''
        Verifies version string retrieval.
        '''
        self.assertEqual(self.decoder.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
