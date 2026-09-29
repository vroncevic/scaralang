# -*- coding: UTF-8 -*-

'''
Module
    motor_wire_mode_test.py
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
    Unit tests for MotorWireMode protocol enumeration.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorWireModeTest(TestCase):
    '''
        Tests for MotorWireMode IntEnum members.
    '''

    def test_members(self) -> None:
        '''Verifies all enum member values.'''
        self.assertEqual(MotorWireMode.OPEN_LOOP.value, 0)
        self.assertEqual(MotorWireMode.CLOSED_LOOP.value, 1)

    def test_instantiation_from_int(self) -> None:
        '''Verifies instantiation from integer values.'''
        self.assertEqual(MotorWireMode(0), MotorWireMode.OPEN_LOOP)
        self.assertEqual(MotorWireMode(1), MotorWireMode.CLOSED_LOOP)
