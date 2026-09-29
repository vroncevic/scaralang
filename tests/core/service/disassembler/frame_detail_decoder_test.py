# -*- coding: UTF-8 -*-

'''
Module
    frame_detail_decoder_test.py
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
    Unit tests for FrameDetailDecoder service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.disassembler.frame_detail_decoder import FrameDetailDecoder
from scaralang.core.service.disassembler.iframe_detail_decoder import IFrameDetailDecoder
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameDetailDecoder(TestCase):
    '''Test suite verifying FrameDetailDecoder translation operations.'''

    def setUp(self) -> None:
        '''Initializes unpacker and decoder fixtures.'''
        self.unpacker: BinaryPayloadUnpacker = BinaryPayloadUnpacker()
        self.decoder: FrameDetailDecoder = FrameDetailDecoder(unpacker=self.unpacker)

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.decoder, IFrameDetailDecoder))

    def test_decode_msg_name(self) -> None:
        '''Verifies decoding message ID to symbolic name.'''
        self.assertEqual(
            self.decoder.decode_msg_name(msg_id=int(MessageId.CMD_HOME)),
            'CMD_HOME',
        )
        self.assertEqual(
            self.decoder.decode_msg_name(msg_id=99999),
            'UNKNOWN',
        )

    def test_decode_system_command(self) -> None:
        '''Verifies decoding system command messages.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
            payload=b'',
            crc16=0,
        )
        detail: str = self.decoder.decode_detail(frame=frame)
        self.assertEqual(detail, 'HOME')

    def test_decode_wait_command(self) -> None:
        '''Verifies decoding wait delay frames.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_WAIT,
            seq_num=2,
            payload=(500).to_bytes(4, byteorder='little'),
            crc16=0,
        )
        detail: str = self.decoder.decode_detail(frame=frame)
        self.assertEqual(detail, 'WAIT 500ms')

    def test_decode_tool_command(self) -> None:
        '''Verifies decoding pneumatic tool pump frames.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_TOOL_PUMP,
            seq_num=3,
            payload=bytes([0, 1]),
            crc16=0,
        )
        detail: str = self.decoder.decode_detail(frame=frame)
        self.assertEqual(detail, 'PUMP ON')

    def test_decode_motor_config_closed_loop(self) -> None:
        '''Verifies decoding motor config closed loop frames.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            seq_num=5,
            payload=bytes([1, 0x0F]),
            crc16=0,
        )
        detail: str = self.decoder.decode_detail(frame=frame)
        self.assertEqual(detail, 'CONFIG MOTOR CLOSED_LOOP')

    def test_decode_motor_config_open_loop(self) -> None:
        '''Verifies decoding motor config open loop frames.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            seq_num=6,
            payload=bytes([0, 0x0F]),
            crc16=0,
        )
        detail: str = self.decoder.decode_detail(frame=frame)
        self.assertEqual(detail, 'CONFIG MOTOR OPEN_LOOP')

    def test_decode_fallback(self) -> None:
        '''Verifies hex string decoding for arbitrary payloads.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_PING,
            seq_num=4,
            payload=b'\x12\x34',
            crc16=0,
        )
        detail: str = self.decoder.decode_detail(frame=frame)
        self.assertEqual(detail, 'payload=1234')


if __name__ == '__main__':
    main()
