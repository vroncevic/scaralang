# -*- coding: UTF-8 -*-

'''
Module
    packer.py
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
    Concrete implementation of binary wire frame packager and serializer.
'''

from __future__ import annotations

from struct import pack
from typing import ClassVar

from scaralang.core.model.protocol.binary_delimiter import BinaryDelimiter
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.protocol.binary.checksum.crc16_ccitt import Crc16Ccitt
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFramePacker:
    '''
        Assembles and checksums wire protocol binary frames and serializes wire bytes.

        It defines:

            :attributes:
                | BYTE_MASK - Bitmask isolating single byte values (0xFF).
                | WORD_MASK - Bitmask isolating 16-bit word values (0xFFFF).
                | SOF1 - First start of frame byte delimiter (0xAA).
                | SOF2 - Second start of frame byte delimiter (0x55).
                | EOF - End of frame byte delimiter (0x0D).
                | HEADER_FORMAT - Struct format for 3-byte frame header (msg, seq, len).
                | TRAILER_FORMAT - Struct format for 3-byte frame trailer (crc16, eof).
            :methods:
                | build_frame - Encodes generic binary command frame with CRC16.
                | pack_frame - Serializes complete frame with delimiters and CRC.
                | get_version - Returns component version string.
    '''

    BYTE_MASK: ClassVar[int] = 0xFF
    WORD_MASK: ClassVar[int] = 0xFFFF
    SOF1: ClassVar[int] = int(BinaryDelimiter.SOF1)
    SOF2: ClassVar[int] = int(BinaryDelimiter.SOF2)
    EOF: ClassVar[int] = int(BinaryDelimiter.EOF)
    HEADER_FORMAT: ClassVar[str] = str(BinaryStructFormat.HEADER)
    TRAILER_FORMAT: ClassVar[str] = str(BinaryStructFormat.TRAILER)

    def build_frame(
        self,
        *,
        msg_id: MessageId,
        seq_num: int,
        payload: bytes = b'',
    ) -> BinaryFrame:
        '''
            Constructs and checksums a complete wire protocol BinaryFrame.

            :param msg_id: Command message identifier.
            :param seq_num: Cyclic sequence index (0 - 255).
            :param payload: Raw body bytes (0 to 64 bytes).
            :return: Fully assembled BinaryFrame with valid CRC16.
            :exceptions: None.
        '''
        safe_seq: int = seq_num & self.BYTE_MASK
        header_data: bytes = pack(
            self.HEADER_FORMAT, int(msg_id), safe_seq, len(payload) & self.BYTE_MASK
        )
        crc: int = Crc16Ccitt.calculate(header_data + payload)

        return BinaryFrame(msg_id=msg_id, seq_num=safe_seq, payload=payload, crc16=crc)

    def pack_frame(self, *, frame: BinaryFrame) -> bytes:
        '''
            Encodes the frame into a byte string according to wire format.

            :param frame: BinaryFrame instance to serialize.
            :return: Formatted bytes: SOF1 + SOF2 + MSG + SEQ + LEN + DATA + CRC + EOF.
            :exceptions: None.
        '''
        header: bytes = pack(
            self.HEADER_FORMAT,
            int(frame.msg_id),
            frame.seq_num & self.BYTE_MASK,
            len(frame.payload) & self.BYTE_MASK,
        )
        trailer: bytes = pack(self.TRAILER_FORMAT, frame.crc16 & self.WORD_MASK, self.EOF)

        return bytes([self.SOF1, self.SOF2]) + header + frame.payload + trailer

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
