# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_packer.py
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
    Defines IBinaryFramePacker protocol for low-level wire frame assembly and packaging.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFramePacker(Protocol):
    '''
        Structural protocol defining binary wire frame assembly and serialization contracts.

        It defines:

            :methods:
                | build_frame - Assembles a generic binary frame with CRC16.
                | pack_frame - Serializes a BinaryFrame into raw wire bytes with delimiters.
                | get_version - Returns packer version string.
    '''

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
        '''

    def pack_frame(self, *, frame: BinaryFrame) -> bytes:
        '''
            Encodes the frame into a byte string according to wire format.

            :param frame: BinaryFrame instance to serialize.
            :return: Formatted bytes: SOF1 + SOF2 + MSG + SEQ + LEN + DATA + CRC + EOF.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
