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
    Unit tests for ReplSessionContextFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.repl.context import ReplSessionContext
from scaralang.core.service.repl.context.factory import ReplSessionContextFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplSessionContextFactory(TestCase):
    '''Test cases verifying ReplSessionContextFactory instantiation and versioning.'''

    def test_create(self) -> None:
        '''Verifies factory creates fully-initialized ReplSessionContext instance.'''
        ctx: ReplSessionContext = ReplSessionContextFactory.create()
        self.assertIsInstance(ctx, ReplSessionContext)
        self.assertEqual(ctx.pose.current_x, 0.0)
        self.assertEqual(ctx.pose.current_y, 0.0)
        self.assertEqual(ctx.pose.current_z, 0.0)
        self.assertEqual(ctx.pose.current_theta4, 0.0)
        self.assertFalse(ctx.elbow_left)
        self.assertEqual(ctx.speed_mode, SpeedMode.WORK)
        self.assertEqual(ctx.zone_mode, ZoneMode.FINE)
        self.assertFalse(ctx.pump_active)
        self.assertFalse(ctx.valve_active)

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid version string.'''
        version: str = ReplSessionContextFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.1.0')


if __name__ == '__main__':
    main()
