# -*- coding: UTF-8 -*-

'''
Module
    motor_config_factory_test.py
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
    Unit tests for MotorConfigFactory service component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.motor.motor_config import MotorConfig
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorConfigFactoryTest(TestCase):
    '''
        Tests for MotorConfigFactory instantiation, parsing, and wire mapping methods.
    '''

    def test_create(self) -> None:
        '''Verifies create factory method builds expected MotorConfig.'''
        cfg: MotorConfig = MotorConfigFactory.create(
            mode=MotorDriveMode.CLOSED_LOOP,
            interface_type=MotorInterfaceType.SERIAL,
            axis_mask=AxisMask.J1,
        )
        self.assertEqual(cfg.mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(cfg.interface_type, MotorInterfaceType.SERIAL)
        self.assertEqual(cfg.axis_mask, AxisMask.J1)

    def test_create_open_loop(self) -> None:
        '''Verifies create_open_loop creates default open loop config.'''
        cfg: MotorConfig = MotorConfigFactory.create_open_loop()
        self.assertEqual(cfg.mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(cfg.interface_type, MotorInterfaceType.STEP_DIR)
        self.assertEqual(cfg.axis_mask, AxisMask.ALL)

    def test_create_closed_loop(self) -> None:
        '''Verifies create_closed_loop creates default closed loop config.'''
        cfg: MotorConfig = MotorConfigFactory.create_closed_loop()
        self.assertEqual(cfg.mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(cfg.interface_type, MotorInterfaceType.CAN_BUS)
        self.assertEqual(cfg.axis_mask, AxisMask.ALL)

    def test_parse_drive_mode_valid(self) -> None:
        '''Verifies parsing recognized drive mode names and aliases.'''
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('OPEN_LOOP'), MotorDriveMode.OPEN_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('open_loop'), MotorDriveMode.OPEN_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('OPEN'), MotorDriveMode.OPEN_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('0'), MotorDriveMode.OPEN_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('CLOSED_LOOP'), MotorDriveMode.CLOSED_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('closed_loop'), MotorDriveMode.CLOSED_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('CLOSED'), MotorDriveMode.CLOSED_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.parse_drive_mode('1'), MotorDriveMode.CLOSED_LOOP
        )

    def test_parse_drive_mode_invalid(self) -> None:
        '''Verifies ScaraSemanticError on invalid mode strings.'''
        with self.assertRaises(ScaraSemanticError):
            MotorConfigFactory.parse_drive_mode('UNKNOWN_MODE')

    def test_is_valid_drive_mode(self) -> None:
        '''Verifies is_valid_drive_mode checks.'''
        self.assertTrue(MotorConfigFactory.is_valid_drive_mode('OPEN_LOOP'))
        self.assertTrue(MotorConfigFactory.is_valid_drive_mode('CLOSED_LOOP'))
        self.assertTrue(MotorConfigFactory.is_valid_drive_mode('OPEN'))
        self.assertTrue(MotorConfigFactory.is_valid_drive_mode('CLOSED'))
        self.assertFalse(MotorConfigFactory.is_valid_drive_mode('INVALID'))

    def test_supported_mode_strings(self) -> None:
        '''Verifies supported mode strings tuple contains canonical modes.'''
        supported = MotorConfigFactory.supported_mode_strings()
        self.assertIn('OPEN_LOOP', supported)
        self.assertIn('CLOSED_LOOP', supported)
        self.assertIn('OPEN', supported)
        self.assertIn('CLOSED', supported)

    def test_to_wire_mode(self) -> None:
        '''Verifies mapping to protocol wire values.'''
        self.assertEqual(
            MotorConfigFactory.to_wire_mode(MotorDriveMode.OPEN_LOOP),
            MotorWireMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorConfigFactory.to_wire_mode(MotorDriveMode.CLOSED_LOOP),
            MotorWireMode.CLOSED_LOOP,
        )

    def test_from_wire_mode(self) -> None:
        '''Verifies mapping from protocol wire values to domain modes.'''
        self.assertEqual(
            MotorConfigFactory.from_wire_mode(0), MotorDriveMode.OPEN_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.from_wire_mode(1), MotorDriveMode.CLOSED_LOOP
        )
        self.assertEqual(
            MotorConfigFactory.from_wire_mode(MotorWireMode.OPEN_LOOP),
            MotorDriveMode.OPEN_LOOP,
        )
        self.assertEqual(
            MotorConfigFactory.from_wire_mode(MotorWireMode.CLOSED_LOOP),
            MotorDriveMode.CLOSED_LOOP,
        )

    def test_resolve_interface_type_defaults(self) -> None:
        '''Verifies default interface type resolution based on motor mode.'''
        self.assertEqual(
            MotorConfigFactory.resolve_interface_type(mode=MotorDriveMode.OPEN_LOOP),
            MotorInterfaceType.STEP_DIR,
        )
        self.assertEqual(
            MotorConfigFactory.resolve_interface_type(mode=MotorDriveMode.CLOSED_LOOP),
            MotorInterfaceType.CAN_BUS,
        )

    def test_resolve_interface_type_custom(self) -> None:
        '''Verifies explicit interface type resolution.'''
        self.assertEqual(
            MotorConfigFactory.resolve_interface_type(
                mode=MotorDriveMode.OPEN_LOOP, raw_interface='SERIAL'
            ),
            MotorInterfaceType.SERIAL,
        )
        self.assertEqual(
            MotorConfigFactory.resolve_interface_type(
                mode=MotorDriveMode.CLOSED_LOOP, raw_interface='step_dir'
            ),
            MotorInterfaceType.STEP_DIR,
        )

    def test_resolve_interface_type_invalid(self) -> None:
        '''Verifies ScaraSemanticError on unrecognized interface strings.'''
        with self.assertRaises(ScaraSemanticError):
            MotorConfigFactory.resolve_interface_type(
                mode=MotorDriveMode.OPEN_LOOP, raw_interface='ETHERNET'
            )

    def test_supported_interface_strings(self) -> None:
        '''Verifies supported interface names tuple.'''
        supported = MotorConfigFactory.supported_interface_strings()
        self.assertIn('STEP_DIR', supported)
        self.assertIn('CAN_BUS', supported)
        self.assertIn('SERIAL', supported)

    def test_get_version(self) -> None:
        '''Verifies version string retrieval.'''
        self.assertEqual(MotorConfigFactory.get_version(), '1.0.5')


if __name__ == '__main__':
    main()
