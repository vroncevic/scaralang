# -*- coding: UTF-8 -*-

'''
Module
    motor_drive_mode_resolver_test.py
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
    Unit tests for MotorDriveModeResolver service component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.service.motor.motor_drive_mode_resolver import MotorDriveModeResolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorDriveModeResolverTest(TestCase):
    '''
        Tests for MotorDriveModeResolver parsing, validation, and supported strings.
    '''

    def test_parse_drive_mode_valid(self) -> None:
        '''Verifies parsing recognized drive mode names and aliases.'''
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('OPEN_LOOP'),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('open_loop'),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('OPEN'),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('0'),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('CLOSED_LOOP'),
            MotorDriveMode.CLOSED_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('closed_loop'),
            MotorDriveMode.CLOSED_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('CLOSED'),
            MotorDriveMode.CLOSED_LOOP,
        )
        self.assertEqual(
            MotorDriveModeResolver.parse_drive_mode('1'),
            MotorDriveMode.CLOSED_LOOP,
        )

    def test_parse_drive_mode_invalid(self) -> None:
        '''Verifies ScaraSemanticError on invalid mode strings.'''
        with self.assertRaises(ScaraSemanticError):
            MotorDriveModeResolver.parse_drive_mode('UNKNOWN_MODE')

    def test_is_valid_drive_mode(self) -> None:
        '''Verifies is_valid_drive_mode checks.'''
        self.assertTrue(MotorDriveModeResolver.is_valid_drive_mode('OPEN_LOOP'))
        self.assertTrue(MotorDriveModeResolver.is_valid_drive_mode('CLOSED_LOOP'))
        self.assertTrue(MotorDriveModeResolver.is_valid_drive_mode('OPEN'))
        self.assertTrue(MotorDriveModeResolver.is_valid_drive_mode('CLOSED'))
        self.assertFalse(MotorDriveModeResolver.is_valid_drive_mode('INVALID'))

    def test_supported_mode_strings(self) -> None:
        '''Verifies supported mode strings tuple contains canonical modes.'''
        supported = MotorDriveModeResolver.supported_mode_strings()
        self.assertIn('OPEN_LOOP', supported)
        self.assertIn('CLOSED_LOOP', supported)
        self.assertIn('OPEN', supported)
        self.assertIn('CLOSED', supported)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertEqual(MotorDriveModeResolver.get_version(), '1.0.7')
