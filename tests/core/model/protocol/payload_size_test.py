# -*- coding: UTF-8 -*-

'''
Module
    payload_size_test.py
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
    Unit tests for BinaryPayloadSize protocol enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.payload_size import BinaryPayloadSize

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPayloadSizeTest(TestCase):
    '''
        Unit tests validating BinaryPayloadSize enumeration members, integer values, and lookups.
    '''

    def test_member_values(self) -> None:
        '''
            Verify integer byte lengths for wire protocol payloads.

            :exceptions: None.
        '''
        self.assertEqual(BinaryPayloadSize.OVERRIDE.value, 1)
        self.assertEqual(BinaryPayloadSize.TOOL_CMD.value, 2)
        self.assertEqual(BinaryPayloadSize.CONFIG_MOTOR.value, 2)
        self.assertEqual(BinaryPayloadSize.ACK.value, 2)
        self.assertEqual(BinaryPayloadSize.NACK.value, 2)
        self.assertEqual(BinaryPayloadSize.WAIT.value, 4)
        self.assertEqual(BinaryPayloadSize.JOG_SHORT.value, 5)
        self.assertEqual(BinaryPayloadSize.MOVE_EVENT.value, 5)
        self.assertEqual(BinaryPayloadSize.FAULT_EVENT.value, 6)
        self.assertEqual(BinaryPayloadSize.JOG_FULL.value, 9)
        self.assertEqual(BinaryPayloadSize.STATUS.value, 19)
        self.assertEqual(BinaryPayloadSize.JOINT_STEPS.value, 22)
        self.assertEqual(BinaryPayloadSize.DIAGNOSTICS.value, 56)

    def test_int_comparison(self) -> None:
        '''
            Verify that IntEnum directly compares with integer lengths.

            :exceptions: None.
        '''
        self.assertEqual(BinaryPayloadSize.OVERRIDE, 1)
        self.assertEqual(BinaryPayloadSize.TOOL_CMD, 2)
        self.assertEqual(BinaryPayloadSize.JOINT_STEPS, 22)
        self.assertEqual(BinaryPayloadSize.DIAGNOSTICS, 56)

    def test_lookup_by_value(self) -> None:
        '''
            Verify enum lookup from integer byte lengths.

            :exceptions: None.
        '''
        self.assertIs(BinaryPayloadSize(1), BinaryPayloadSize.OVERRIDE)
        self.assertIs(BinaryPayloadSize(4), BinaryPayloadSize.WAIT)
        self.assertIs(BinaryPayloadSize(6), BinaryPayloadSize.FAULT_EVENT)
        self.assertIs(BinaryPayloadSize(9), BinaryPayloadSize.JOG_FULL)
        self.assertIs(BinaryPayloadSize(19), BinaryPayloadSize.STATUS)
        self.assertIs(BinaryPayloadSize(22), BinaryPayloadSize.JOINT_STEPS)
        self.assertIs(BinaryPayloadSize(56), BinaryPayloadSize.DIAGNOSTICS)

    def test_invalid_value_raises_value_error(self) -> None:
        '''
            Verify that undefined payload length raises ValueError.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            BinaryPayloadSize(999)


if __name__ == '__main__':
    main()
