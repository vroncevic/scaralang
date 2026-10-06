# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_assembler_test.py
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
    Unit tests for BinaryFrameAssembler.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scaralang.infrastructure.communication.protocol.binary.checksum.crc16_ccitt import Crc16Ccitt
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_assembler import BinaryFrameAssembler
from scaralang.infrastructure.communication.protocol.binary.parser.ibinary_frame_assembler import IBinaryFrameAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFrameAssembler(TestCase):
    '''
        Test suite verifying BinaryFrameAssembler frame assembly and CRC validation.

        It defines:

            :methods:
                | setUp - Initializes assembler fixture.
                | test_structural_typing - Verifies protocol adherence.
                | test_name - Verifies assembler name property.
                | test_assemble_valid_frame - Verifies assembly with valid CRC.
                | test_assemble_corrupted_crc - Verifies rejection of invalid CRC.
                | test_assemble_empty_payload - Verifies assembly with zero-length payload.
                | test_assemble_invalid_message_id - Verifies rejection of invalid message ID.
    '''

    def setUp(self) -> None:
        '''Initializes assembler fixture.'''
        self.assembler = BinaryFrameAssembler()

    def test_structural_typing(self) -> None:
        '''Verifies instance satisfies IBinaryFrameAssembler protocol.'''
        self.assertIsInstance(self.assembler, IBinaryFrameAssembler)

    def test_assemble_valid_frame(self) -> None:
        '''Verifies valid frame assembly with correct CRC.'''
        msg_id: int = int(MessageId.CMD_HOME)
        seq_num: int = 1
        payload: bytes = b'\x01\x02\x03\x04'
        payload_len: int = len(payload)

        header: bytes = pack(str(BinaryStructFormat.HEADER), msg_id, seq_num, payload_len)
        expected_crc: int = Crc16Ccitt.calculate(header + payload)
        crc_lo: int = expected_crc & 0xFF
        crc_hi: int = (expected_crc >> 8) & 0xFF

        frame: BinaryFrame | None = self.assembler.assemble(
            msg_id=msg_id,
            seq_num=seq_num,
            payload=payload,
            crc_bytes=(crc_lo, crc_hi),
        )

        self.assertIsNotNone(frame)
        if frame is not None:
            self.assertEqual(frame.msg_id, MessageId.CMD_HOME)
            self.assertEqual(frame.seq_num, seq_num)
            self.assertEqual(frame.payload, payload)
            self.assertEqual(frame.crc16, expected_crc)

    def test_assemble_corrupted_crc(self) -> None:
        '''Verifies assembler returns None when CRC is corrupted.'''
        msg_id: int = int(MessageId.CMD_HOME)
        seq_num: int = 2
        payload: bytes = b'\x05\x06'
        payload_len: int = len(payload)

        header: bytes = pack(str(BinaryStructFormat.HEADER), msg_id, seq_num, payload_len)
        correct_crc: int = Crc16Ccitt.calculate(header + payload)
        corrupted_crc: int = correct_crc ^ 0xFFFF
        crc_lo: int = corrupted_crc & 0xFF
        crc_hi: int = (corrupted_crc >> 8) & 0xFF

        frame: BinaryFrame | None = self.assembler.assemble(
            msg_id=msg_id,
            seq_num=seq_num,
            payload=payload,
            crc_bytes=(crc_lo, crc_hi),
        )

        self.assertIsNone(frame)

    def test_assemble_empty_payload(self) -> None:
        '''Verifies assembler handles empty payload with valid CRC.'''
        msg_id: int = int(MessageId.CMD_ENABLE)
        seq_num: int = 3
        payload: bytes = b''
        payload_len: int = 0

        header: bytes = pack(str(BinaryStructFormat.HEADER), msg_id, seq_num, payload_len)
        expected_crc: int = Crc16Ccitt.calculate(header + payload)
        crc_lo: int = expected_crc & 0xFF
        crc_hi: int = (expected_crc >> 8) & 0xFF

        frame: BinaryFrame | None = self.assembler.assemble(
            msg_id=msg_id,
            seq_num=seq_num,
            payload=payload,
            crc_bytes=(crc_lo, crc_hi),
        )

        self.assertIsNotNone(frame)
        if frame is not None:
            self.assertEqual(frame.msg_id, MessageId.CMD_ENABLE)
            self.assertEqual(frame.seq_num, seq_num)
            self.assertEqual(frame.payload, b'')
            self.assertEqual(frame.crc16, expected_crc)

    def test_name(self) -> None:
        '''Verifies name property returns assembler identifier.'''
        self.assertEqual(self.assembler.name, 'binary_frame_assembler')

    def test_assemble_invalid_message_id(self) -> None:
        '''Verifies assembler returns None when message ID is invalid.'''
        invalid_msg_id: int = 0xFF
        seq_num: int = 1
        payload: bytes = b''
        header: bytes = pack(str(BinaryStructFormat.HEADER), invalid_msg_id, seq_num, 0)
        expected_crc: int = Crc16Ccitt.calculate(header + payload)
        crc_lo: int = expected_crc & 0xFF
        crc_hi: int = (expected_crc >> 8) & 0xFF

        frame = self.assembler.assemble(
            msg_id=invalid_msg_id,
            seq_num=seq_num,
            payload=payload,
            crc_bytes=(crc_lo, crc_hi),
        )
        self.assertIsNone(frame)


if __name__ == '__main__':
    main()
