# -*- coding: UTF-8 -*-

'''
Module
    compiler_speed_state_test.py
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
    Unit tests for CompilerSpeedState model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.compiler.compiler_speed_state import CompilerSpeedState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerSpeedStateTest(TestCase):
    '''
        Validates CompilerSpeedState default initialization, custom values, and mutation.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default initialization of speed parameters.
        '''
        spd = CompilerSpeedState()
        self.assertEqual(spd.speed_rapid, 150.0)
        self.assertEqual(spd.speed_work, 40.0)
        self.assertEqual(spd.current_speed, 40.0)
        self.assertEqual(spd.active_accel, 300.0)
        self.assertEqual(spd.speed_override_pct, 100.0)

    def test_custom_values(self) -> None:
        '''
            Verifies custom values assignment on instantiation.
        '''
        spd = CompilerSpeedState(
            speed_rapid=200.0,
            speed_work=60.0,
            current_speed=50.0,
            active_accel=500.0,
            speed_override_pct=80.0,
        )
        self.assertEqual(spd.speed_rapid, 200.0)
        self.assertEqual(spd.speed_work, 60.0)
        self.assertEqual(spd.current_speed, 50.0)
        self.assertEqual(spd.active_accel, 500.0)
        self.assertEqual(spd.speed_override_pct, 80.0)

    def test_state_mutation(self) -> None:
        '''
            Verifies in-place mutation of speed parameters.
        '''
        spd = CompilerSpeedState()
        spd.speed_rapid = 180.0
        spd.speed_work = 55.0
        spd.current_speed = 70.0
        spd.active_accel = 400.0
        spd.speed_override_pct = 90.0

        self.assertEqual(spd.speed_rapid, 180.0)
        self.assertEqual(spd.speed_work, 55.0)
        self.assertEqual(spd.current_speed, 70.0)
        self.assertEqual(spd.active_accel, 400.0)
        self.assertEqual(spd.speed_override_pct, 90.0)


if __name__ == '__main__':
    main()
