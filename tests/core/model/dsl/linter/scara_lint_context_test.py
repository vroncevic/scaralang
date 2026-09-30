# -*- coding: UTF-8 -*-

'''
Module
    scara_lint_context_test.py
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
    Unit testing for ScaraLintContext domain model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLintContextTest(TestCase):
    '''
        Validates ScaraLintContext simulation tracking and mutable state management.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default initialization flags of the linting context.
        '''
        ctx = ScaraLintContext()
        self.assertFalse(ctx.is_homed)
        self.assertFalse(ctx.motion_occurred)
        self.assertFalse(ctx.pump_on)
        self.assertFalse(ctx.valve_on)
        self.assertEqual(ctx.zone_mode, ZoneMode.FINE)
        self.assertAlmostEqual(ctx.zone_radius, 0.0)
        self.assertEqual(ctx.last_coords, ())

    def test_custom_values(self) -> None:
        '''
            Verifies initialization with specific tracking flags.
        '''
        ctx = ScaraLintContext(
            is_homed=True,
            motion_occurred=True,
            pump_on=True,
            valve_on=False,
            zone_mode=ZoneMode.BLEND,
            zone_radius=5.0,
            last_coords=(100.0, 50.0, 20.0),
        )
        self.assertTrue(ctx.is_homed)
        self.assertTrue(ctx.motion_occurred)
        self.assertTrue(ctx.pump_on)
        self.assertFalse(ctx.valve_on)
        self.assertEqual(ctx.zone_mode, ZoneMode.BLEND)
        self.assertAlmostEqual(ctx.zone_radius, 5.0)
        self.assertEqual(ctx.last_coords, (100.0, 50.0, 20.0))

    def test_state_mutation(self) -> None:
        '''
            Verifies in-place mutation of linting state attributes.
        '''
        ctx = ScaraLintContext()
        ctx.is_homed = True
        ctx.motion_occurred = True
        ctx.pump_on = True
        ctx.valve_on = True
        ctx.last_coords = (150.0, 0.0, 20.0)

        self.assertTrue(ctx.is_homed)
        self.assertTrue(ctx.motion_occurred)
        self.assertTrue(ctx.pump_on)
        self.assertTrue(ctx.valve_on)
        self.assertEqual(ctx.last_coords, (150.0, 0.0, 20.0))


if __name__ == '__main__':
    main()
