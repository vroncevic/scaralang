# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_codec.py
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
    Defines IBinaryFrameCodec structural protocol for stream parsing and packet packing.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFrameCodec(Protocol):
    '''
        Structural protocol defining binary stream encoding and decoding operations.

        It defines:

            :methods:
                | feed_bytes - Parses incoming raw bytes and returns completed frames.
                | pack_frame - Serializes a BinaryFrame into wire format byte sequence.
                | reset - Resets decoder state machine.
                | get_version - Returns codec version string.
    '''

    def feed_bytes(self, data: bytes) -> tuple[BinaryFrame, ...]:
        '''
            Pumps incoming raw stream bytes through the decoder.

            :param data: Input bytes slice.
            :return: Tuple of fully decoded and validated BinaryFrames.
            :exceptions: None.
        '''

    def pack_frame(self, frame: BinaryFrame) -> bytes:
        '''
            Encodes a BinaryFrame into serialized wire protocol bytes with CRC and delimiters.

            :param frame: BinaryFrame instance to serialize.
            :return: Formatted wire byte sequence.
            :exceptions: None.
        '''

    def reset(self) -> None:
        '''
            Resets parser state machine and clears internal byte buffers.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the codec version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
