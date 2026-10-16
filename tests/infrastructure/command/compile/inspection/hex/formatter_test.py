# -*- coding: UTF-8 -*-

'''
Module
    formatter_test.py
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
    Unit tests for HexStreamFormatter.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.hex.formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.hex.iformatter import IHexStreamFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHexStreamFormatter(TestCase):
    '''Test cases verifying HexStreamFormatter formatting operations.'''

    def setUp(self) -> None:
        '''Initializes formatter instance.'''
        self.formatter = HexStreamFormatter()

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol conformance.'''
        self.assertIsInstance(self.formatter, IHexStreamFormatter)

    def test_get_version(self) -> None:
        '''Verifies version string retrieval.'''
        self.assertEqual(self.formatter.get_version(), '1.0.9')

    def test_format_bytes(self) -> None:
        '''Verifies formatting raw byte sequence into uppercase hex tokens.'''
        data = bytes([0xAA, 0x55, 0x01, 0xFF])
        result = self.formatter.format_bytes(data=data)
        self.assertEqual(result, 'AA 55 01 FF')

    def test_format_preview_short(self) -> None:
        '''Verifies format_preview returns full hex if length <= max_bytes.'''
        data = bytes([0x01, 0x02, 0x03])
        result = self.formatter.format_preview(data=data, max_bytes=8)
        self.assertEqual(result, '01 02 03')

    def test_format_preview_truncated(self) -> None:
        '''Verifies format_preview truncates with ellipsis if length > max_bytes.'''
        data = bytes(range(20))
        result = self.formatter.format_preview(data=data, max_bytes=8)
        self.assertIn('...', result)
        self.assertTrue(result.startswith('00 01 02 03'))
        self.assertTrue(result.endswith('10 11 12 13'))


if __name__ == '__main__':
    main()
