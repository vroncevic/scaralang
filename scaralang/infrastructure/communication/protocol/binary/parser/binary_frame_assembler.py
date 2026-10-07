# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_assembler.py
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
    Assembles and validates BinaryFrame instances from parsed header and payload.
'''

from __future__ import annotations

from struct import pack
from typing import ClassVar

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scaralang.infrastructure.communication.protocol.binary.checksum.crc16_ccitt import Crc16Ccitt

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameAssembler:
    '''
        Assembles BinaryFrame from validated header, payload, and CRC-16 checksum.

        It defines:

            :attributes:
                | name - Identifier name of the assembler.
                | HEADER_FORMAT - Struct format for 3-byte frame header (<BBB).
            :methods:
                | assemble - Validates CRC-16 and constructs BinaryFrame if valid.
    '''

    HEADER_FORMAT: ClassVar[str] = str(BinaryStructFormat.HEADER)

    @property
    def name(self) -> str:
        '''
            Gets the assembler identifier name.

            :return: Assembler name string.
        '''
        return 'binary_frame_assembler'

    def assemble(
        self,
        *,
        msg_id: int,
        seq_num: int,
        payload: bytes,
        crc_bytes: tuple[int, int],
    ) -> BinaryFrame | None:
        '''
            Validates CRC-16-CCITT and constructs a BinaryFrame if valid.

            :param msg_id: Message identifier integer.
            :param seq_num: Packet sequence number integer.
            :param payload: Contiguous payload bytes.
            :param crc_bytes: Tuple of (crc_lo, crc_hi) bytes.
            :return: Assembled BinaryFrame if CRC is valid, None otherwise.
        '''
        header_bytes: bytes = pack(
            self.HEADER_FORMAT,
            msg_id,
            seq_num,
            len(payload),
        )
        rx_crc: int = (crc_bytes[0] & 0xFF) | ((crc_bytes[1] & 0xFF) << 8)

        if not Crc16Ccitt.verify(header_bytes + payload, rx_crc):
            return None

        try:
            resolved_msg_id = MessageId(msg_id)

        except ValueError:
            return None

        return BinaryFrame(
            msg_id=resolved_msg_id,
            seq_num=seq_num,
            payload=payload,
            crc16=rx_crc,
        )
