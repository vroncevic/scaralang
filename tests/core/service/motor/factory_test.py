# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for MotorFactory service component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.motor.motor_config import MotorConfig
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType
from scaralang.core.service.motor.factory import MotorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorFactoryTest(TestCase):
    '''
        Tests for MotorFactory instantiation and version methods.
    '''

    def test_create(self) -> None:
        '''Verifies create factory method builds expected MotorConfig.'''
        cfg: MotorConfig = MotorFactory.create(
            mode=MotorDriveMode.CLOSED_LOOP,
            interface_type=MotorInterfaceType.SERIAL,
            axis_mask=AxisMask.J1,
        )
        self.assertEqual(cfg.mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(cfg.interface_type, MotorInterfaceType.SERIAL)
        self.assertEqual(cfg.axis_mask, AxisMask.J1)

    def test_create_open_loop(self) -> None:
        '''Verifies create builds open loop config with STEP_DIR.'''
        cfg: MotorConfig = MotorFactory.create(
            mode=MotorDriveMode.OPEN_LOOP,
            interface_type=MotorInterfaceType.STEP_DIR,
            axis_mask=AxisMask.ALL,
        )
        self.assertEqual(cfg.mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(cfg.interface_type, MotorInterfaceType.STEP_DIR)
        self.assertEqual(cfg.axis_mask, AxisMask.ALL)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertEqual(MotorFactory.get_version(), '1.0.9')
