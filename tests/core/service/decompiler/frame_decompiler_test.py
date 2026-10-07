# -*- coding: UTF-8 -*-

'''
Module
    frame_decompiler_test.py
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
    Unit tests for FrameDecompiler service.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.decompiler.frame_decompiler import FrameDecompiler
from scaralang.core.service.decompiler.iframe_decompiler import IFrameDecompiler
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameDecompiler(TestCase):
    '''Test suite verifying FrameDecompiler translation operations.'''

    def setUp(self) -> None:
        '''Initializes kinematics, transmission, and frame decompiler fixtures.'''
        kinematics = KinematicsServiceFactory.create_default()
        transmission = JointStepTransmissionConverterFactory.create_default()
        unpacker = BinaryPayloadUnpackerFactory.create()
        self.decompiler: FrameDecompiler = FrameDecompiler(
            kinematics=kinematics,
            transmission=transmission,
            unpacker=unpacker,
        )

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.decompiler, IFrameDecompiler))

    def test_get_version(self) -> None:
        '''Verifies frame decompiler version string retrieval.'''
        self.assertEqual(self.decompiler.get_version(), '1.0.7')

    def test_decompile_system_commands(self) -> None:
        '''Verifies decoding system lifecycle commands.'''
        cases: list[tuple[MessageId, str]] = [
            (MessageId.CMD_HOME, 'HOME'),
            (MessageId.CMD_ENABLE, 'ENABLE'),
            (MessageId.CMD_DISABLE, 'DISABLE'),
            (MessageId.CMD_ESTOP, 'ESTOP'),
            (MessageId.CMD_HOLD, 'HOLD'),
            (MessageId.CMD_RESUME, 'RESUME'),
        ]
        for msg_id, expected in cases:
            frame = BinaryFrame(seq_num=1, msg_id=msg_id, payload=b'', crc16=0)
            self.assertEqual(self.decompiler.decompile_frame(frame=frame), expected)

    def test_decompile_tool_commands(self) -> None:
        '''Verifies decoding pump and valve actuation commands.'''
        pump_on = BinaryFrame(
            seq_num=1,
            msg_id=MessageId.CMD_TOOL_PUMP,
            payload=pack('<BB', 0, 1),
            crc16=0,
        )
        self.assertEqual(self.decompiler.decompile_frame(frame=pump_on), 'PUMP ON')

        pump_off = BinaryFrame(
            seq_num=2,
            msg_id=MessageId.CMD_TOOL_PUMP,
            payload=pack('<BB', 0, 0),
            crc16=0,
        )
        self.assertEqual(self.decompiler.decompile_frame(frame=pump_off), 'PUMP OFF')

        valve_on = BinaryFrame(
            seq_num=3,
            msg_id=MessageId.CMD_TOOL_VALVE,
            payload=pack('<BB', 1, 1),
            crc16=0,
        )
        self.assertEqual(self.decompiler.decompile_frame(frame=valve_on), 'VALVE ON')

    def test_decompile_wait_command(self) -> None:
        '''Verifies decoding wait delay command.'''
        frame = BinaryFrame(
            seq_num=1,
            msg_id=MessageId.CMD_WAIT,
            payload=pack('<I', 750),
            crc16=0,
        )
        self.assertEqual(self.decompiler.decompile_frame(frame=frame), 'WAIT 750')

    def test_decompile_override_command(self) -> None:
        '''Verifies decoding override feedrate command.'''
        frame = BinaryFrame(
            seq_num=1,
            msg_id=MessageId.CMD_OVERRIDE,
            payload=bytes([80]),
            crc16=0,
        )
        self.assertEqual(self.decompiler.decompile_frame(frame=frame), 'OVERRIDE 80')

    def test_decompile_config_motor_command(self) -> None:
        '''Verifies decoding motor config command.'''
        frame = BinaryFrame(
            seq_num=1,
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            payload=pack('<BB', 0, 0x0F),
            crc16=0,
        )
        self.assertEqual(
            self.decompiler.decompile_frame(frame=frame),
            'CONFIG MOTOR OPEN_LOOP',
        )

    def test_decompile_move_joint_steps(self) -> None:
        '''Verifies decoding joint steps frame into Cartesian MOVE_L instruction.'''
        payload: bytes = pack('<iiiiIH', 0, 0, 0, 0, 10000, 1)
        frame = BinaryFrame(
            seq_num=1,
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            payload=payload,
            crc16=0,
        )
        result: str = self.decompiler.decompile_frame(frame=frame)
        self.assertTrue(result.startswith('MOVE_L X '))
        self.assertIn(' Y ', result)
        self.assertIn(' Z 0.00 ', result)
        self.assertIn(' PHI 0.00', result)

    def test_decompile_jog_joint(self) -> None:
        '''Verifies decoding joint jog command.'''
        frame = BinaryFrame(
            seq_num=1,
            msg_id=MessageId.CMD_JOG_JOINT,
            payload=pack('<Bi', 1, -250),
            crc16=0,
        )
        self.assertEqual(self.decompiler.decompile_frame(frame=frame), 'JOG_JOINT J2 -250')

    def test_decompile_unmapped_frame(self) -> None:
        '''Verifies unmapped frame returns empty string.'''
        frame = BinaryFrame(seq_num=1, msg_id=MessageId.CMD_NONE, payload=b'', crc16=0)
        self.assertEqual(self.decompiler.decompile_frame(frame=frame), '')


if __name__ == '__main__':
    main()
