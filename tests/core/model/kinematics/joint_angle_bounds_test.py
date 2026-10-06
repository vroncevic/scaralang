# -*- coding: UTF-8 -*-

'''
Module
    joint_angle_bounds_test.py
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
    Unit tests for pure data model JointAngleBounds.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.joint_angle_bounds import JointAngleBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointAngleBounds(TestCase):
    '''Unit tests validating JointAngleBounds initialization, slots, and immutability.'''

    def test_instantiation(self) -> None:
        '''Verify field values on initialization.'''
        bounds = JointAngleBounds(
            j1_min_rad=-2.61799,
            j1_max_rad=2.61799,
            j2_min_rad=-2.61799,
            j2_max_rad=2.61799,
        )
        self.assertEqual(bounds.j1_min_rad, -2.61799)
        self.assertEqual(bounds.j1_max_rad, 2.61799)
        self.assertEqual(bounds.j2_min_rad, -2.61799)
        self.assertEqual(bounds.j2_max_rad, 2.61799)

    def test_immutability(self) -> None:
        '''Verify frozen dataclass prevents mutation.'''
        bounds = JointAngleBounds(
            j1_min_rad=-2.5,
            j1_max_rad=2.5,
            j2_min_rad=-2.8,
            j2_max_rad=2.8,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(bounds, 'j1_max_rad', 3.0)

    def test_equality(self) -> None:
        '''Verify value-object equality semantics.'''
        bounds1 = JointAngleBounds(
            j1_min_rad=-2.5,
            j1_max_rad=2.5,
            j2_min_rad=-2.8,
            j2_max_rad=2.8,
        )
        bounds2 = JointAngleBounds(
            j1_min_rad=-2.5,
            j1_max_rad=2.5,
            j2_min_rad=-2.8,
            j2_max_rad=2.8,
        )
        bounds3 = JointAngleBounds(
            j1_min_rad=-2.5,
            j1_max_rad=2.5,
            j2_min_rad=-2.8,
            j2_max_rad=3.0,
        )
        self.assertEqual(bounds1, bounds2)
        self.assertNotEqual(bounds1, bounds3)


if __name__ == '__main__':
    main()
