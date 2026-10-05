# -*- coding: UTF-8 -*-

'''
Module
    motor_interface_type_test.py
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
    Unit tests for MotorInterfaceType domain enumeration.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorInterfaceTypeTest(TestCase):
    '''
        Tests for MotorInterfaceType StrEnum members.
    '''

    def test_members(self) -> None:
        '''Verifies all enum member names and values.'''
        self.assertEqual(MotorInterfaceType.STEP_DIR.value, 'STEP_DIR')
        self.assertEqual(MotorInterfaceType.CAN_BUS.value, 'CAN_BUS')
        self.assertEqual(MotorInterfaceType.SERIAL.value, 'SERIAL')

    def test_instantiation_from_str(self) -> None:
        '''Verifies instantiation from string representations.'''
        self.assertEqual(MotorInterfaceType('STEP_DIR'), MotorInterfaceType.STEP_DIR)
        self.assertEqual(MotorInterfaceType('CAN_BUS'), MotorInterfaceType.CAN_BUS)
        self.assertEqual(MotorInterfaceType('SERIAL'), MotorInterfaceType.SERIAL)
