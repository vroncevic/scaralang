# -*- coding: UTF-8 -*-

'''
Module
    iframe_trailer_formatter.py
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
    Defines structural interface protocol for binary frame trailer presentation formatting.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFrameTrailerFormatter(Protocol):
    '''
        Structural interface protocol for formatting wire frame trailer and CRC checksum.

        It defines:

            :methods:
                | format_trailer - Formats frame CRC16 and EOF delimiter.
                | get_version - Returns the interface protocol version identifier.
    '''

    def format_trailer(self, *, crc16: int) -> str:
        '''
            Formats wire frame trailer fields including CRC16 and EOF delimiter.

            :param crc16: 16-bit CRC checksum value.
            :return: Formatted trailer presentation string.
        '''

    def get_version(self) -> str:
        '''
            Returns the interface protocol version identifier.

            :return: The protocol version string.
        '''
