# -*- coding: UTF-8 -*-

'''
Module
    hex_stream_formatter.py
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
    Defines HexStreamFormatter formatting bytes into hexadecimal tokens and truncated previews.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class HexStreamFormatter:
    '''
        Formats raw binary bytes into space-separated uppercase hex tokens and previews.

        It defines:

            :methods:
                | format_bytes - Formats raw bytes into space-separated uppercase hex string.
                | format_preview - Formats truncated preview of byte sequence.
    '''

    def format_bytes(self, *, data: bytes) -> str:
        '''
            Formats raw byte sequence into space-separated uppercase hex tokens.

            :param data: Raw byte sequence to format.
            :return: Formatted hex string.
        '''
        return ' '.join(f'{b:02X}' for b in data)

    def format_preview(self, *, data: bytes, max_bytes: int = 16) -> str:
        '''
            Formats truncated preview of byte sequence with ellipsis if length exceeds limit.

            :param data: Raw byte sequence.
            :param max_bytes: Maximum byte count before inserting ellipsis.
            :return: Formatted hex string or preview.
        '''
        if len(data) <= max_bytes:
            return self.format_bytes(data=data)

        half: int = max(1, max_bytes // 2)
        head: str = self.format_bytes(data=data[:half])
        tail: str = self.format_bytes(data=data[-half:])
        return f'{head} ... {tail}'
