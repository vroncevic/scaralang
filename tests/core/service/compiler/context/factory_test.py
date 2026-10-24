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
    Unit tests for CompilerContextFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.compiler.context import CompilerContext
from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.service.compiler.context.factory import CompilerContextFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerContextFactoryTest(TestCase):
    '''
        Validates creation of CompilerContext instances by CompilerContextFactory.
    '''

    def test_create(self) -> None:
        '''
            Verifies creation of initialized CompilerContext with default properties.
        '''
        context: CompilerContext = CompilerContextFactory.create()
        self.assertIsInstance(context, CompilerContext)
        self.assertAlmostEqual(context.pose.current_x, 150.0)
        self.assertAlmostEqual(context.pose.current_y, 0.0)
        self.assertAlmostEqual(context.pose.current_z, 20.0)
        self.assertAlmostEqual(context.pose.current_phi, 0.0)
        self.assertEqual(context.pose.elbow_config, ElbowConfig.RIGHT)
        self.assertAlmostEqual(context.speed.speed_rapid, 150.0)
        self.assertAlmostEqual(context.speed.speed_work, 40.0)
        self.assertAlmostEqual(context.speed.current_speed, 40.0)
        self.assertAlmostEqual(context.speed.active_accel, 300.0)
        self.assertAlmostEqual(context.speed.speed_override_pct, 100.0)
        self.assertEqual(context.blend.zone_mode, ZoneMode.FINE)
        self.assertAlmostEqual(context.blend.zone_radius, 0.0)
        self.assertAlmostEqual(context.active_frame.origin.x, 0.0)
        self.assertAlmostEqual(context.active_frame.origin.y, 0.0)
        self.assertAlmostEqual(context.active_frame.origin.z, 0.0)
        self.assertAlmostEqual(context.active_frame.angle_deg, 0.0)
        self.assertEqual(context.tool_orient_mode, ToolOrientMode.FIXED)
        self.assertEqual(context.motor_drive_mode, MotorDriveMode.OPEN_LOOP)
        self.assertEqual(len(context.pallets), 0)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.
        '''
        version = CompilerContextFactory.get_version()
        self.assertEqual(version, '1.1.1')


if __name__ == '__main__':
    main()
