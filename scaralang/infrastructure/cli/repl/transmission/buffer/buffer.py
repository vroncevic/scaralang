# -*- coding: UTF-8 -*-

'''
Module
    buffer.py
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
    Concrete implementation of REPL transmission logging buffer.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransmissionBuffer:
    '''
        Defines class TransmissionBuffer implementing ITransmissionBuffer contract structurally.
        Concrete in-memory buffer storing transmitted binary frame packets.

        It defines:

            :attributes:
                | _frames - Internal list of raw frame byte packets.
            :methods:
                | __init__ - Initializes empty transmission buffer.
                | append - Appends serialized frame bytes to buffer.
                | get_frames - Returns shallow copy of logged frame bytes.
                | clear - Resets the transmission buffer.
    '''

    _frames: list[bytes]

    def __init__(self) -> None:
        '''
            Initializes empty transmission buffer.

            :return: None.
            :exceptions: None.
        '''
        self._frames = []

    def append(self, *, frame_bytes: bytes) -> None:
        '''
            Appends serialized frame bytes to buffer.

            :param frame_bytes: Serialized binary frame byte stream.
            :return: None.
            :exceptions: None.
        '''
        self._frames.append(frame_bytes)

    def get_frames(self) -> list[bytes]:
        '''
            Returns shallow copy of logged frame bytes.

            :return: List of transmitted byte frames.
            :exceptions: None.
        '''
        return list(self._frames)

    def clear(self) -> None:
        '''
            Clears all buffered frame bytes.

            :return: None.
            :exceptions: None.
        '''
        self._frames.clear()
