# -*- coding: UTF-8 -*-

'''
Module
    motor_interface_resolver_test.py
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
    Unit tests for MotorInterfaceResolver service component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType
from scaralang.core.service.motor.motor_interface_resolver import MotorInterfaceResolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorInterfaceResolverTest(TestCase):
    '''
        Tests for MotorInterfaceResolver resolving, validation, and defaults.
    '''

    def test_resolve_interface_defaults(self) -> None:
        '''Verifies mode-aware default interface resolution when unspecified.'''
        self.assertEqual(
            MotorInterfaceResolver.resolve_interface_type(
                mode=MotorDriveMode.OPEN_LOOP
            ),
            MotorInterfaceType.STEP_DIR,
        )
        self.assertEqual(
            MotorInterfaceResolver.resolve_interface_type(
                mode=MotorDriveMode.CLOSED_LOOP
            ),
            MotorInterfaceType.CAN_BUS,
        )

    def test_resolve_interface_explicit(self) -> None:
        '''Verifies resolving explicit interface strings case-insensitively.'''
        self.assertEqual(
            MotorInterfaceResolver.resolve_interface_type(
                mode=MotorDriveMode.OPEN_LOOP,
                raw_interface='CAN_BUS',
            ),
            MotorInterfaceType.CAN_BUS,
        )
        self.assertEqual(
            MotorInterfaceResolver.resolve_interface_type(
                mode=MotorDriveMode.CLOSED_LOOP,
                raw_interface='step_dir',
            ),
            MotorInterfaceType.STEP_DIR,
        )
        self.assertEqual(
            MotorInterfaceResolver.resolve_interface_type(
                mode=MotorDriveMode.OPEN_LOOP,
                raw_interface='SERIAL',
            ),
            MotorInterfaceType.SERIAL,
        )

    def test_resolve_interface_invalid(self) -> None:
        '''Verifies ScaraSemanticError on unrecognized interface strings.'''
        with self.assertRaises(ScaraSemanticError):
            MotorInterfaceResolver.resolve_interface_type(
                mode=MotorDriveMode.OPEN_LOOP,
                raw_interface='ETHERNET',
            )

    def test_supported_interface_strings(self) -> None:
        '''Verifies supported interface strings tuple.'''
        supported = MotorInterfaceResolver.supported_interface_strings()
        self.assertIn('STEP_DIR', supported)
        self.assertIn('CAN_BUS', supported)
        self.assertIn('SERIAL', supported)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertEqual(MotorInterfaceResolver.get_version(), '1.0.6')
