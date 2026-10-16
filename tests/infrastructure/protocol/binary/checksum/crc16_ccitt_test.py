# -*- coding: UTF-8 -*-

'''
Module
    crc16_ccitt_test.py
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
    Unit tests for Crc16Ccitt checksum calculation engine.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.infrastructure.protocol.binary.checksum.crc16_ccitt import Crc16Ccitt

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCrc16Ccitt(TestCase):
    '''
        Test cases verifying Crc16Ccitt checksum algorithm.

        It defines:

            :methods:
                | test_constants - Verifies ClassVar algorithmic constants.
                | test_calculate_empty - Verifies checksum of empty buffer.
                | test_update_incremental - Verifies incremental updates equal bulk calculate.
                | test_verify_valid_and_invalid - Verifies verification against expected CRC.
    '''

    def test_constants(self) -> None:
        '''Verifies ClassVar algorithmic constants defined on Crc16Ccitt.'''
        self.assertEqual(Crc16Ccitt.INITIAL_SEED, 0xFFFF)
        self.assertEqual(Crc16Ccitt.POLYNOMIAL, 0x1021)
        self.assertEqual(Crc16Ccitt.BYTE_MASK, 0xFF)
        self.assertEqual(Crc16Ccitt.BYTE_SHIFT, 8)
        self.assertEqual(Crc16Ccitt.BITS_PER_BYTE, 8)
        self.assertEqual(Crc16Ccitt.MSB_MASK, 0x8000)
        self.assertEqual(Crc16Ccitt.BIT_SHIFT, 1)

    def test_calculate_empty(self) -> None:
        '''Verifies checksum of empty byte sequence equals initial seed.'''
        crc = Crc16Ccitt.calculate(b'')
        self.assertEqual(crc, Crc16Ccitt.INITIAL_SEED)

    def test_update_incremental(self) -> None:
        '''Verifies incremental single-byte updates match bulk calculation.'''
        data = b'SCARA_ROBOTICS_FRAME_2026'
        bulk_crc = Crc16Ccitt.calculate(data)

        running_crc = Crc16Ccitt.INITIAL_SEED
        for b in data:
            running_crc = Crc16Ccitt.update(running_crc, b)

        self.assertEqual(running_crc, bulk_crc)

    def test_verify_valid_and_invalid(self) -> None:
        '''Verifies verify returns True on match and False on mismatch.'''
        data = b'TEST_PAYLOAD'
        crc = Crc16Ccitt.calculate(data)

        self.assertTrue(Crc16Ccitt.verify(data, crc))
        self.assertFalse(Crc16Ccitt.verify(data, crc ^ 0x0001))
        self.assertFalse(Crc16Ccitt.verify(b'CORRUPTED', crc))


if __name__ == '__main__':
    main()
