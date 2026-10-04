# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_assembler.py
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
    Abstract interface for binary frame assembler and validator.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFrameAssembler(Protocol):
    '''
        Protocol defining contract for binary frame assembly and CRC validation.

        It defines:

            :attributes:
                | name - Identifier name of the assembler.
            :methods:
                | assemble - Validates CRC-16 and constructs BinaryFrame instance.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the assembler identifier name.

            :return: Assembler name string.
        '''

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
            :return: Assembled BinaryFrame if valid, None otherwise.
        '''
