# -*- coding: UTF-8 -*-

'''
Module
    system_decoder_test.py
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
    Unit tests for SystemDecoder component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.disassembler.frame.decoder.idecoder import IFramePayloadDecoder
from scaralang.core.service.disassembler.frame.decoder.system_decoder import SystemDecoder
from scaralang.infrastructure.protocol.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSystemDecoder(TestCase):
    '''
    Test cases verifying SystemDecoder operations.

    It defines:

        :methods:
            | setUp - Sets up decoder fixture.
            | test_protocol_conformance - Verifies protocol check.
            | test_can_decode - Verifies message ID matching.
            | test_decode_home - Verifies decoding home command.
            | test_decode_motor_config - Verifies decoding motor configuration.
            | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
        Sets up decoder with concrete unpacker fixture.
        '''
        self.unpacker: BinaryActuatorPayloadUnpacker = (
            BinaryActuatorPayloadUnpacker()
        )
        self.decoder: SystemDecoder = SystemDecoder(
            unpacker=self.unpacker
        )

    def test_protocol_conformance(self) -> None:
        '''
        Verifies decoder satisfies IFramePayloadDecoder protocol.
        '''
        self.assertIsInstance(self.decoder, IFramePayloadDecoder)

    def test_can_decode(self) -> None:
        '''
        Verifies can_decode matches motor config and system commands.
        '''
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_HOME)))
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_CONFIG_MOTOR)))
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_ESTOP)))
        self.assertFalse(self.decoder.can_decode(msg_id=int(MessageId.CMD_TOOL_PUMP)))

    def test_decode_home(self) -> None:
        '''
        Verifies decoding system home frame.
        '''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
            payload=b'',
            crc16=0,
        )
        self.assertEqual(self.decoder.decode(frame=frame), 'HOME')

    def test_decode_motor_config(self) -> None:
        '''
        Verifies decoding motor config closed loop and open loop frames.
        '''
        frame_closed: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            seq_num=5,
            payload=bytes([1, 0x0F]),
            crc16=0,
        )
        self.assertEqual(
            self.decoder.decode(frame=frame_closed),
            'CONFIG MOTOR CLOSED_LOOP',
        )

        frame_open: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            seq_num=6,
            payload=bytes([0, 0x0F]),
            crc16=0,
        )
        self.assertEqual(
            self.decoder.decode(frame=frame_open),
            'CONFIG MOTOR OPEN_LOOP',
        )

    def test_get_version(self) -> None:
        '''
        Verifies version string retrieval.
        '''
        self.assertEqual(self.decoder.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
