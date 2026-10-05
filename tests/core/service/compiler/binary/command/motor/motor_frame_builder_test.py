# -*- coding: UTF-8 -*-

'''
Module
    motor_frame_builder_test.py
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
    Unit tests for MotorFrameBuilder.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode
from scaralang.core.service.compiler.binary.command.motor.imotor_frame_builder import IMotorFrameBuilder
from scaralang.core.service.compiler.binary.command.motor.motor_frame_builder import MotorFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotorFrameBuilder(TestCase):
    '''
        Test cases verifying MotorFrameBuilder functionality.

        It defines:

            :methods:
                | setUp - Initializes fixtures with frame builder.
                | test_structural_conformance - Verifies protocol check.
                | test_get_version - Verifies get_version returns valid version string.
                | test_build_motor_frame_open_loop - Verifies OPEN_LOOP frame.
                | test_build_motor_frame_closed_loop - Verifies CLOSED_LOOP frame.
                | test_build_motor_frame_default - Verifies default when arg is empty.
    '''

    def setUp(self) -> None:
        '''Sets up frame builder and motor frame builder fixtures.'''
        self.frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        self.motor_builder = MotorFrameBuilder(frame_builder=self.frame_builder)

    def test_structural_conformance(self) -> None:
        '''Verifies structural conformance to IMotorFrameBuilder.'''
        self.assertIsInstance(self.motor_builder, IMotorFrameBuilder)

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid version string.'''
        self.assertEqual(self.motor_builder.get_version(), '1.0.4')


    def test_build_motor_frame_open_loop(self) -> None:
        '''Verifies building binary frame for OPEN_LOOP motor configuration.'''
        frame: BinaryFrame = self.motor_builder.build_motor_frame(
            arg='OPEN_LOOP',
            seq_num=1,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 1)
        self.assertEqual(len(frame.payload), 2)
        self.assertEqual(frame.payload[0], MotorWireMode.OPEN_LOOP.value)
        self.assertEqual(frame.payload[1], 0x0F)

    def test_build_motor_frame_closed_loop(self) -> None:
        '''Verifies building binary frame for CLOSED_LOOP motor configuration.'''
        frame: BinaryFrame = self.motor_builder.build_motor_frame(
            arg='CLOSED_LOOP',
            seq_num=2,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 2)
        self.assertEqual(len(frame.payload), 2)
        self.assertEqual(frame.payload[0], MotorWireMode.CLOSED_LOOP.value)
        self.assertEqual(frame.payload[1], 0x0F)

    def test_build_motor_frame_default(self) -> None:
        '''Verifies default open loop when arg is empty.'''
        frame: BinaryFrame = self.motor_builder.build_motor_frame(
            arg='',
            seq_num=3,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(frame.seq_num, 3)
        self.assertEqual(frame.payload[0], MotorWireMode.OPEN_LOOP.value)


if __name__ == '__main__':
    main()
