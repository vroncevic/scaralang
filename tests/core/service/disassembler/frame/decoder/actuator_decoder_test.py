# -*- coding: UTF-8 -*-

'''
Module
    actuator_decoder_test.py
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
    Unit tests for ActuatorDecoder component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.disassembler.frame.decoder.actuator_decoder import ActuatorDecoder
from scaralang.core.service.disassembler.frame.decoder.idecoder import IFramePayloadDecoder
from scaralang.infrastructure.protocol.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestActuatorDecoder(TestCase):
    '''
    Test cases verifying ActuatorDecoder operations.

    It defines:

        :methods:
            | setUp - Sets up decoder fixture.
            | test_protocol_conformance - Verifies protocol check.
            | test_can_decode - Verifies message ID matching.
            | test_decode_wait - Verifies decoding wait delay.
            | test_decode_tool_pump - Verifies decoding tool pump.
            | test_decode_tool_valve - Verifies decoding tool valve.
            | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
        Sets up decoder with concrete unpacker fixture.
        '''
        self.unpacker: BinaryActuatorPayloadUnpacker = (
            BinaryActuatorPayloadUnpacker()
        )
        self.decoder: ActuatorDecoder = ActuatorDecoder(
            unpacker=self.unpacker
        )

    def test_protocol_conformance(self) -> None:
        '''
        Verifies decoder satisfies IFramePayloadDecoder protocol.
        '''
        self.assertIsInstance(self.decoder, IFramePayloadDecoder)

    def test_can_decode(self) -> None:
        '''
        Verifies can_decode matches pump, valve, and wait commands.
        '''
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_TOOL_PUMP)))
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_TOOL_VALVE)))
        self.assertTrue(self.decoder.can_decode(msg_id=int(MessageId.CMD_WAIT)))
        self.assertFalse(self.decoder.can_decode(msg_id=int(MessageId.CMD_HOME)))

    def test_decode_wait(self) -> None:
        '''
        Verifies decoding wait delay payload.
        '''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_WAIT,
            seq_num=2,
            payload=(500).to_bytes(4, byteorder='little'),
            crc16=0,
        )
        self.assertEqual(self.decoder.decode(frame=frame), 'WAIT 500ms')

    def test_decode_tool_pump(self) -> None:
        '''
        Verifies decoding pump on/off payloads.
        '''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_TOOL_PUMP,
            seq_num=3,
            payload=bytes([0, 1]),
            crc16=0,
        )
        self.assertEqual(self.decoder.decode(frame=frame), 'PUMP ON')

    def test_decode_tool_valve(self) -> None:
        '''
        Verifies decoding valve on/off payloads.
        '''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_TOOL_VALVE,
            seq_num=4,
            payload=bytes([0, 0]),
            crc16=0,
        )
        self.assertEqual(self.decoder.decode(frame=frame), 'VALVE OFF')

    def test_get_version(self) -> None:
        '''
        Verifies version string retrieval.
        '''
        self.assertEqual(self.decoder.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
