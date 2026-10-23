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
    Unit tests for LintContextFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.linter.context import LintContext
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.service.linter.context.factory import LintContextFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LintContextFactoryTest(TestCase):
    '''
        Validates creation of LintContext instances by LintContextFactory.
    '''

    def test_create(self) -> None:
        '''
            Verifies creation of initialized LintContext with default properties.
        '''
        context: LintContext = LintContextFactory.create()
        self.assertIsInstance(context, LintContext)
        self.assertFalse(context.is_homed)
        self.assertFalse(context.motion_occurred)
        self.assertFalse(context.tool_state.pump_on)
        self.assertFalse(context.tool_state.valve_on)
        self.assertEqual(context.zone_mode, ZoneMode.FINE)
        self.assertAlmostEqual(context.zone_radius, 0.0)
        self.assertEqual(context.last_coords, ())
        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.
        '''
        version = LintContextFactory.get_version()
        self.assertEqual(version, '1.1.0')


if __name__ == '__main__':
    main()
