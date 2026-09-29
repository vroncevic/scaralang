# -*- coding: UTF-8 -*-

'''
Module
    motor_config_test.py
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
    Unit tests for MotorConfig domain dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.motor.motor_config import MotorConfig
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorConfigTest(TestCase):
    '''
        Tests for MotorConfig dataclass creation and immutability.
    '''

    def test_creation_attributes(self) -> None:
        '''Verifies MotorConfig attributes match constructor arguments.'''
        cfg = MotorConfig(
            mode=MotorDriveMode.CLOSED_LOOP,
            interface_type=MotorInterfaceType.CAN_BUS,
            axis_mask=AxisMask.ALL,
        )
        self.assertEqual(cfg.mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(cfg.interface_type, MotorInterfaceType.CAN_BUS)
        self.assertEqual(cfg.axis_mask, AxisMask.ALL)

    def test_immutability(self) -> None:
        '''Verifies MotorConfig is frozen and cannot be mutated.'''
        cfg = MotorConfig(
            mode=MotorDriveMode.OPEN_LOOP,
            interface_type=MotorInterfaceType.STEP_DIR,
            axis_mask=AxisMask.ALL,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(cfg, 'mode', MotorDriveMode.CLOSED_LOOP)
