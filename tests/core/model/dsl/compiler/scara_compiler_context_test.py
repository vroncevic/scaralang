# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_context_test.py
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
    Unit testing for ScaraCompilerContext domain model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.dsl.macro.pallet_definition import PalletDefinition
from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.elbow_config import ElbowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompilerContextTest(TestCase):
    '''
        Validates ScaraCompilerContext state tracking, frame delegation, and pallet storage.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default compiler context state.
        '''
        context = ScaraCompilerContext()
        self.assertAlmostEqual(context.current_x, 150.0)
        self.assertAlmostEqual(context.current_y, 0.0)
        self.assertAlmostEqual(context.current_z, 20.0)
        self.assertAlmostEqual(context.current_phi, 0.0)
        self.assertAlmostEqual(context.speed_rapid, 150.0)
        self.assertAlmostEqual(context.speed_work, 40.0)
        self.assertAlmostEqual(context.current_speed, 40.0)
        self.assertAlmostEqual(context.active_accel, 300.0)
        self.assertEqual(context.elbow_config, ElbowConfig.RIGHT)
        self.assertEqual(context.tool_orient_mode, ToolOrientMode.FIXED)
        self.assertEqual(context.zone_mode, ZoneMode.FINE)
        self.assertAlmostEqual(context.zone_radius, 0.0)
        self.assertAlmostEqual(context.speed_override_pct, 100.0)
        self.assertEqual(len(context.pallets), 0)
        self.assertAlmostEqual(context.active_frame.x, 0.0)
        self.assertAlmostEqual(context.active_frame.y, 0.0)
        self.assertAlmostEqual(context.active_frame.angle_deg, 0.0)

    def test_active_frame_storage(self) -> None:
        '''
            Verifies active_frame state storage in compiler context.
        '''
        context = ScaraCompilerContext()
        context.active_frame = WorkFrame(x=100.0, y=50.0, angle_deg=90.0)

        self.assertAlmostEqual(context.active_frame.x, 100.0)
        self.assertAlmostEqual(context.active_frame.y, 50.0)
        self.assertAlmostEqual(context.active_frame.angle_deg, 90.0)

    def test_pallet_registration_and_retrieval(self) -> None:
        '''
            Verifies that strongly-typed PalletDefinition entities can be stored and retrieved.
        '''
        context = ScaraCompilerContext()
        pallet = PalletDefinition(
            name='TRAY',
            rows=2,
            cols=2,
            dx=10.0,
            dy=10.0,
            start_x=50.0,
            start_y=60.0,
        )
        context.pallets[pallet.name] = pallet
        self.assertIn('TRAY', context.pallets)
        self.assertEqual(context.pallets['TRAY'].rows, 2)

    def test_state_mutation(self) -> None:
        '''
            Verifies mutation of speed, pose, and acceleration settings.
        '''
        context = ScaraCompilerContext()
        context.current_x = 200.0
        context.current_y = 50.0
        context.current_z = 10.0
        context.current_speed = 80.0
        context.elbow_config = ElbowConfig.LEFT

        self.assertAlmostEqual(context.current_x, 200.0)
        self.assertAlmostEqual(context.current_y, 50.0)
        self.assertAlmostEqual(context.current_z, 10.0)
        self.assertAlmostEqual(context.current_speed, 80.0)
        self.assertEqual(context.elbow_config, ElbowConfig.LEFT)


if __name__ == '__main__':
    main()
