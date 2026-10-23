# -*- coding: UTF-8 -*-

'''
Module
    speed_test.py
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
    Unit tests for pure data model SpeedLimits.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.speed import SpeedLimits

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpeedTest(TestCase):
    '''
        Unit tests validating SpeedLimits initialization, slots, and immutability.

        It defines:

            :methods:
                | test_instantiation - Verifies field values on initialization.
                | test_immutability - Verifies frozen dataclass prevents mutation.
                | test_equality - Verifies value-object equality semantics.
    '''

    def test_instantiation(self) -> None:
        '''
            Verify field values on initialization.

            :exceptions: None.
        '''
        limits = SpeedLimits(
            min_speed=1.0,
            max_speed=200.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
        )
        self.assertEqual(limits.min_speed, 1.0)
        self.assertEqual(limits.max_speed, 200.0)
        self.assertEqual(limits.default_speed, 50.0)
        self.assertEqual(limits.default_accel, 100.0)
        self.assertEqual(limits.max_accel, 500.0)

    def test_immutability(self) -> None:
        '''
            Verify frozen dataclass prevents mutation.

            :exceptions: None.
        '''
        limits = SpeedLimits(
            min_speed=1.0,
            max_speed=200.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(limits, 'max_speed', 300.0)

    def test_equality(self) -> None:
        '''
            Verify value-object equality semantics.

            :exceptions: None.
        '''
        limits1 = SpeedLimits(
            min_speed=1.0,
            max_speed=200.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
        )
        limits2 = SpeedLimits(
            min_speed=1.0,
            max_speed=200.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
        )
        limits3 = SpeedLimits(
            min_speed=1.0,
            max_speed=300.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
        )
        self.assertEqual(limits1, limits2)
        self.assertNotEqual(limits1, limits3)


if __name__ == '__main__':
    main()
