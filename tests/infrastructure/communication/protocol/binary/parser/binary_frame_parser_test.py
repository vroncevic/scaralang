# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_parser_test.py
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
    Unit tests for BinaryFrameParser.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_assembler_factory import BinaryFrameAssemblerFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.parser_state import ParserState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFrameParser(TestCase):
    '''
        Test suite verifying BinaryFrameParser state transitions, buffering, and decoding.

        It defines:

            :methods:
                | setUp - Initializes parser and builder fixtures.
                | test_structural_typing - Verifies parser satisfies IBinaryFrameParser.
                | test_feed_valid_frame - Verifies parsing complete valid binary frames.
                | test_feed_byte_step_by_step - Verifies step-by-step FSM state progression.
                | test_corrupted_crc_frame - Verifies frame rejection on CRC mismatch.
                | test_invalid_sof_bytes - Verifies FSM resynchronization on invalid header bytes.
                | test_payload_length_overflow - Verifies parser resets on oversized payload length.
                | test_reset - Verifies manual parser reset back to initial search state.
    '''

    def setUp(self) -> None:
        '''Initializes parser and builder fixtures.'''
        self.builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        self.parser: BinaryFrameParser = BinaryFrameParser(
            assembler=BinaryFrameAssemblerFactory.create()
        )

    def test_structural_typing(self) -> None:
        '''Verifies instance satisfies IBinaryFrameParser protocol.'''
        self.assertIsInstance(self.parser, IBinaryFrameParser)

    def test_feed_valid_frame(self) -> None:
        '''Verifies streaming feed and extraction of a complete binary frame.'''
        frame = self.builder.build_system_cmd(msg_id=MessageId.CMD_HOME, seq_num=7)
        wire_bytes: bytes = self.builder.pack_frame(frame=frame)

        parsed_frames = self.parser.feed_bytes(wire_bytes)
        self.assertEqual(len(parsed_frames), 1)
        self.assertEqual(parsed_frames[0].msg_id, MessageId.CMD_HOME)
        self.assertEqual(parsed_frames[0].seq_num, 7)
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF1)

    def test_feed_byte_step_by_step(self) -> None:
        '''Verifies FSM state transitions on each individual stream byte.'''
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF1)

        # SOF1
        self.assertIsNone(self.parser.feed_byte(0xAA))
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF2)

        # SOF2
        self.assertIsNone(self.parser.feed_byte(0x55))
        self.assertEqual(self.parser.get_state(), ParserState.READ_MSG_ID)

        # MSG_ID (CMD_HOME = 0x01)
        self.assertIsNone(self.parser.feed_byte(int(MessageId.CMD_HOME)))
        self.assertEqual(self.parser.get_state(), ParserState.READ_SEQ_NUM)

        # SEQ_NUM (1)
        self.assertIsNone(self.parser.feed_byte(1))
        self.assertEqual(self.parser.get_state(), ParserState.READ_PAYLOAD_LEN)

        # PAYLOAD_LEN (0) -> transitions directly to READ_CRC_LO
        self.assertIsNone(self.parser.feed_byte(0))
        self.assertEqual(self.parser.get_state(), ParserState.READ_CRC_LO)

    def test_corrupted_crc_frame(self) -> None:
        '''Verifies parser discards frames with invalid CRC checksums.'''
        frame = self.builder.build_system_cmd(msg_id=MessageId.CMD_ENABLE, seq_num=2)
        corrupted_bytes = bytearray(self.builder.pack_frame(frame=frame))
        corrupted_bytes[-3] ^= 0xFF

        parsed_frames = self.parser.feed_bytes(bytes(corrupted_bytes))
        self.assertEqual(len(parsed_frames), 0)
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF1)

    def test_invalid_sof_bytes(self) -> None:
        '''Verifies parser resynchronizes when SOF2 fails.'''
        self.parser.feed_byte(0xAA)
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF2)

        # Non-SOF byte resets to SEARCH_SOF1
        self.parser.feed_byte(0x00)
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF1)

    def test_payload_length_overflow(self) -> None:
        '''Verifies parser resets when payload length exceeds MAX_PAYLOAD_LEN.'''
        self.parser.feed_byte(0xAA)
        self.parser.feed_byte(0x55)
        self.parser.feed_byte(int(MessageId.CMD_HOME))
        self.parser.feed_byte(1)
        # Feed length > 64 (e.g. 100)
        self.parser.feed_byte(100)
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF1)

    def test_reset(self) -> None:
        '''Verifies manual reset clears state back to SEARCH_SOF1.'''
        self.parser.feed_byte(0xAA)
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF2)
        self.parser.reset()
        self.assertEqual(self.parser.get_state(), ParserState.SEARCH_SOF1)


if __name__ == '__main__':
    main()
