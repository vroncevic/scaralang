# -*- coding: UTF-8 -*-

'''
Module
    iresponse_unpacker.py
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
    Defines IBinaryResponsePayloadUnpacker protocol for ACK/NACK response payload deserialization.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryResponsePayloadUnpacker(Protocol):
    '''
        Structural protocol defining response payload deserialization contracts.

        It defines:

            :methods:
                | unpack_ack - Deserializes 2-byte ACK payload into (cmd_id, free_slots).
                | unpack_nack - Deserializes 2-byte NACK payload into (rejected_cmd_id, error_code).
                | get_version - Returns response payload unpacker version string.
    '''

    def unpack_ack(self, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into ACK message ID and queue capacity slots.

            :param data: Input raw binary bytes.
            :return: Tuple containing (acked_message_id, free_slots).
        '''

    def unpack_nack(self, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into NACK message ID and error code.

            :param data: Input raw binary bytes.
            :return: Tuple containing (rejected_message_id, error_code).
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
