# -*- coding: UTF-8 -*-

'''
Module
    binary_delimiter_test.py
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
    Unit tests for BinaryDelimiter protocol enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.binary_delimiter import BinaryDelimiter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryDelimiterTest(TestCase):
    '''Unit tests validating BinaryDelimiter enumeration members, integer values, and lookups.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined binary frame delimiters.'''
        self.assertEqual(len(BinaryDelimiter), 4)

    def test_delimiter_values(self) -> None:
        '''Verify byte values for wire frame delimiters.'''
        self.assertEqual(BinaryDelimiter.SOF1, 0xAA)
        self.assertEqual(BinaryDelimiter.SOF2, 0x55)
        self.assertEqual(BinaryDelimiter.EOF, 0x0D)
        self.assertEqual(BinaryDelimiter.MAX_PAYLOAD_LEN, 64)

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from integer values.'''
        self.assertIs(BinaryDelimiter(0xAA), BinaryDelimiter.SOF1)
        self.assertIs(BinaryDelimiter(0x55), BinaryDelimiter.SOF2)
        self.assertIs(BinaryDelimiter(0x0D), BinaryDelimiter.EOF)
        self.assertIs(BinaryDelimiter(64), BinaryDelimiter.MAX_PAYLOAD_LEN)

    def test_invalid_value_raises_value_error(self) -> None:
        '''Verify that undefined delimiter value raises ValueError.'''
        with self.assertRaises(ValueError):
            BinaryDelimiter(0xFF)


if __name__ == '__main__':
    main()
