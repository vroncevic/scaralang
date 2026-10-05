# -*- coding: UTF-8 -*-

'''
Module
    error_code_test.py
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
    Unit tests for ErrorCode protocol enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.error_code import ErrorCode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ErrorCodeTest(TestCase):
    '''Unit tests validating ErrorCode enumeration members, integer values, and lookups.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined NACK error codes.'''
        self.assertEqual(len(ErrorCode), 10)

    def test_error_code_values(self) -> None:
        '''Verify integer constants for all NACK error classifications.'''
        self.assertEqual(ErrorCode.NONE, 0x00)
        self.assertEqual(ErrorCode.CRC_FAIL, 0x01)
        self.assertEqual(ErrorCode.UNKNOWN_CMD, 0x02)
        self.assertEqual(ErrorCode.INVALID_LENGTH, 0x03)
        self.assertEqual(ErrorCode.QUEUE_FULL, 0x04)
        self.assertEqual(ErrorCode.ESTOP_ACTIVE, 0x05)
        self.assertEqual(ErrorCode.NOT_HELD, 0x06)
        self.assertEqual(ErrorCode.INVALID_JOINT, 0x07)
        self.assertEqual(ErrorCode.HOMING_FAILED, 0x08)
        self.assertEqual(ErrorCode.EXECUTION_FAILED, 0x09)

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from integer values.'''
        self.assertIs(ErrorCode(0x00), ErrorCode.NONE)
        self.assertIs(ErrorCode(0x01), ErrorCode.CRC_FAIL)
        self.assertIs(ErrorCode(0x05), ErrorCode.ESTOP_ACTIVE)

    def test_invalid_value_raises_value_error(self) -> None:
        '''Verify that undefined error code integer raises ValueError.'''
        with self.assertRaises(ValueError):
            ErrorCode(0xFF)


if __name__ == '__main__':
    main()
