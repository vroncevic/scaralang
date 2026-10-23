# -*- coding: UTF-8 -*-

'''
Module
    response.py
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
    Dedicated deserializer decoding ACK and NACK response payloads.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar

from scaralang.core.model.exceptions.protocol import ScaraProtocolError
from scaralang.core.model.protocol.payload_size import BinaryPayloadSize
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryResponsePayloadUnpacker:
    '''
        Deserializer decoding ACK and NACK binary response payloads.

        It defines:

            :attributes:
                | ACK_FORMAT - Struct format for 2-byte ACK payload.
                | NACK_FORMAT - Struct format for 2-byte NACK payload.
            :methods:
                | unpack_ack - Deserializes 2-byte ACK into (acked_cmd_id, free_slots).
                | unpack_nack - Deserializes 2-byte NACK into (rejected_cmd_id, error_code).
                | get_version - Returns component version string.
    '''

    ACK_FORMAT: ClassVar[str] = str(BinaryStructFormat.ACK)
    NACK_FORMAT: ClassVar[str] = str(BinaryStructFormat.NACK)

    def unpack_ack(self, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into ACK message ID and queue capacity slots.

            :param data: Input raw binary bytes.
            :return: Tuple containing (acked_message_id, free_slots).
            :exceptions: ScaraProtocolError if data is less than 2 bytes.
        '''
        if len(data) < BinaryPayloadSize.ACK:
            raise ScaraProtocolError(
                f'ACK payload too short: expected at least '
                f'{int(BinaryPayloadSize.ACK)} bytes, got {len(data)}'
            )

        values: tuple[int, int] = unpack(self.ACK_FORMAT, data[:BinaryPayloadSize.ACK])

        return values[0], values[1]

    def unpack_nack(self, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into NACK message ID and error code.

            :param data: Input raw binary bytes.
            :return: Tuple containing (rejected_message_id, error_code).
            :exceptions: ScaraProtocolError if data is less than 2 bytes.
        '''
        if len(data) < BinaryPayloadSize.NACK:
            raise ScaraProtocolError(
                f'NACK payload too short: expected at least '
                f'{int(BinaryPayloadSize.NACK)} bytes, got {len(data)}'
            )

        values: tuple[int, int] = unpack(self.NACK_FORMAT, data[:BinaryPayloadSize.NACK])

        return values[0], values[1]

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
