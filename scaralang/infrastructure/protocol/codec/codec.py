# -*- coding: UTF-8 -*-

'''
Module
    codec.py
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
    Concrete implementation of binary frame stream codec.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.iparser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameCodec:
    '''
        Stream codec coordinating binary frame parsing and serialization.

        It defines:

            :attributes:
                | _parser - Injected streaming binary frame parser port.
                | _packer - Injected binary wire frame packer port.
            :methods:
                | __init__ - Initializes codec with parser and packer collaborators.
                | feed_bytes - Parses incoming raw bytes and returns completed frames.
                | pack_frame - Serializes a BinaryFrame into wire format byte sequence.
                | reset - Resets decoder state machine.
                | get_version - Returns codec version string.
    '''

    _parser: IBinaryFrameParser
    _packer: IBinaryFramePacker

    def __init__(
        self,
        *,
        parser: IBinaryFrameParser,
        packer: IBinaryFramePacker,
    ) -> None:
        '''
            Initializes codec with parser and packer collaborators.

            :param parser: Streaming binary frame parser port.
            :param packer: Binary wire frame packer port.
            :exceptions: None.
        '''
        self._parser: Final[IBinaryFrameParser] = parser
        self._packer: Final[IBinaryFramePacker] = packer

    def feed_bytes(self, data: bytes) -> tuple[BinaryFrame, ...]:
        '''
            Pumps incoming raw stream bytes through the decoder.

            :param data: Input bytes slice.
            :return: Tuple of fully decoded and validated BinaryFrames.
            :exceptions: None.
        '''
        frames: list[BinaryFrame] = []
        for byte_val in data:
            frame: BinaryFrame | None = self._parser.feed_byte(byte_val)
            if frame is not None:
                frames.append(frame)

        return tuple(frames)

    def pack_frame(self, frame: BinaryFrame) -> bytes:
        '''
            Encodes a BinaryFrame into serialized wire protocol bytes with CRC and delimiters.

            :param frame: BinaryFrame instance to serialize.
            :return: Formatted wire byte sequence.
            :exceptions: None.
        '''
        return self._packer.pack_frame(frame=frame)

    def reset(self) -> None:
        '''
            Resets parser state machine and clears internal byte buffers.

            :exceptions: None.
        '''
        self._parser.reset()

    def get_version(self) -> str:
        '''
            Returns the codec version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
