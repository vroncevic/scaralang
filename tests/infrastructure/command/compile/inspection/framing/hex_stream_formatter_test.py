# -*- coding: UTF-8 -*-

'''
Module
    hex_stream_formatter_test.py
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
    Unit tests for HexStreamFormatter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.framing.ihex_stream_formatter import IHexStreamFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHexStreamFormatter(TestCase):
    '''Test suite verifying HexStreamFormatter formatting operations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        formatter: HexStreamFormatter = HexStreamFormatter()
        self.assertTrue(isinstance(formatter, IHexStreamFormatter))

    def test_format_bytes(self) -> None:
        '''Verifies formatting byte sequences into hex tokens.'''
        formatter: HexStreamFormatter = HexStreamFormatter()
        result: str = formatter.format_bytes(data=bytes([0xAA, 0x55, 0x10, 0x01]))
        self.assertEqual(result, 'AA 55 10 01')

    def test_format_preview_short(self) -> None:
        '''Verifies preview formatting when bytes length is within limit.'''
        formatter: HexStreamFormatter = HexStreamFormatter()
        data: bytes = bytes([0x01, 0x02, 0x03])
        result: str = formatter.format_preview(data=data, max_bytes=8)
        self.assertEqual(result, '01 02 03')

    def test_format_preview_long(self) -> None:
        '''Verifies preview formatting inserts ellipsis when bytes exceed limit.'''
        formatter: HexStreamFormatter = HexStreamFormatter()
        data: bytes = bytes(range(20))
        result: str = formatter.format_preview(data=data, max_bytes=8)
        self.assertIn('...', result)
        self.assertTrue(result.startswith('00 01 02 03'))
        self.assertTrue(result.endswith('10 11 12 13'))


if __name__ == '__main__':
    main()
