# -*- coding: UTF-8 -*-

'''
Module
    repl_session_context_test.py
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
    Unit tests for ReplSessionContext data model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.repl.repl_session_context import ReplSessionContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplSessionContextTest(TestCase):
    '''Unit tests validating ReplSessionContext dataclass default and custom initialization.'''

    def test_default_initialization(self) -> None:
        '''Verify default values on fresh REPL session context.'''
        ctx = ReplSessionContext()
        self.assertEqual(ctx.current_x, 0.0)
        self.assertEqual(ctx.current_y, 0.0)
        self.assertEqual(ctx.current_z, 0.0)
        self.assertEqual(ctx.current_theta4, 0.0)
        self.assertFalse(ctx.elbow_left)
        self.assertEqual(ctx.speed_mode, SpeedMode.WORK)
        self.assertEqual(ctx.zone_mode, ZoneMode.FINE)
        self.assertFalse(ctx.pump_active)
        self.assertFalse(ctx.valve_active)

    def test_custom_initialization(self) -> None:
        '''Verify custom field assignment.'''
        ctx = ReplSessionContext(
            current_x=150.0,
            current_y=75.0,
            current_z=10.0,
            current_theta4=45.0,
            elbow_left=True,
            speed_mode=SpeedMode.RAPID,
            zone_mode=ZoneMode.BLEND,
            pump_active=True,
            valve_active=False
        )
        self.assertEqual(ctx.current_x, 150.0)
        self.assertEqual(ctx.current_y, 75.0)
        self.assertEqual(ctx.current_z, 10.0)
        self.assertEqual(ctx.current_theta4, 45.0)
        self.assertTrue(ctx.elbow_left)
        self.assertEqual(ctx.speed_mode, SpeedMode.RAPID)
        self.assertEqual(ctx.zone_mode, ZoneMode.BLEND)
        self.assertTrue(ctx.pump_active)
        self.assertFalse(ctx.valve_active)

    def test_immutability(self) -> None:
        '''Verify that attributes cannot be modified on frozen dataclass.'''
        ctx = ReplSessionContext()
        with self.assertRaises(AttributeError):
            ctx.current_x = 10.0  # type: ignore[misc]


if __name__ == '__main__':
    main()
