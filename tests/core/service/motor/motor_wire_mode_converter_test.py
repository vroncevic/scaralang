# -*- coding: UTF-8 -*-

'''
Module
    motor_wire_mode_converter_test.py
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
    Unit tests for MotorWireModeConverter service component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode
from scaralang.core.service.motor.motor_wire_mode_converter import MotorWireModeConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorWireModeConverterTest(TestCase):
    '''
        Tests for MotorWireModeConverter wire protocol mapping methods.
    '''

    def test_to_wire_mode(self) -> None:
        '''Verifies mapping domain mode to binary wire mode.'''
        self.assertEqual(
            MotorWireModeConverter.to_wire_mode(MotorDriveMode.OPEN_LOOP),
            MotorWireMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorWireModeConverter.to_wire_mode(MotorDriveMode.CLOSED_LOOP),
            MotorWireMode.CLOSED_LOOP,
        )

    def test_from_wire_mode(self) -> None:
        '''Verifies mapping wire mode int or enum to domain mode.'''
        self.assertEqual(
            MotorWireModeConverter.from_wire_mode(0),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorWireModeConverter.from_wire_mode(1),
            MotorDriveMode.CLOSED_LOOP,
        )
        self.assertEqual(
            MotorWireModeConverter.from_wire_mode(MotorWireMode.OPEN_LOOP),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorWireModeConverter.from_wire_mode(MotorWireMode.CLOSED_LOOP),
            MotorDriveMode.CLOSED_LOOP,
        )

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertEqual(MotorWireModeConverter.get_version(), '1.0.1')
