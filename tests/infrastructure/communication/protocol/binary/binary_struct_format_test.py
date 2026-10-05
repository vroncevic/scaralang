# -*- coding: UTF-8 -*-

'''
Module
    binary_struct_format_test.py
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
    Unit tests for BinaryStructFormat enumeration.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryStructFormat(TestCase):
    '''
        Test cases verifying BinaryStructFormat enumeration.

        It defines:

            :methods:
                | test_binary_struct_formats - Verifies format strings for all frame types.
    '''

    def test_binary_struct_formats(self) -> None:
        '''
            Tests struct format string definitions.
        '''
        self.assertEqual(str(BinaryStructFormat.HEADER), '<BBB')
        self.assertEqual(str(BinaryStructFormat.TRAILER), '<HB')
        self.assertEqual(str(BinaryStructFormat.JOINT_STEPS), '<iiiiIH')
        self.assertEqual(str(BinaryStructFormat.TOOL_CMD), '<BB')
        self.assertEqual(str(BinaryStructFormat.STATUS), '<BBBiiii')
        self.assertEqual(str(BinaryStructFormat.MOVE_EVENT), '<BI')
        self.assertEqual(str(BinaryStructFormat.FAULT_EVENT), '<BBI')
        self.assertEqual(str(BinaryStructFormat.ACK), '<BB')
        self.assertEqual(str(BinaryStructFormat.NACK), '<BB')
        self.assertEqual(str(BinaryStructFormat.DIAGNOSTICS), '<IIIIBBIIIIiiiiBBI')
        self.assertEqual(str(BinaryStructFormat.CONFIG_MOTOR), '<BB')
        self.assertEqual(str(BinaryStructFormat.WAIT), '<I')


if __name__ == '__main__':
    main()
