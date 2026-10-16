# -*- coding: UTF-8 -*-

'''
Module
    cartesian_pose_test.py
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
    Unit tests for pure data model CartesianPose.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.cartesian_pose import CartesianPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCartesianPose(TestCase):
    '''Unit tests validating CartesianPose initialization, slots, and immutability.'''

    def test_instantiation_explicit(self) -> None:
        '''Verify field values and explicit phi on initialization.'''
        pose = CartesianPose(x=150.0, y=-75.5, z=20.0, phi=0.0)
        self.assertEqual(pose.x, 150.0)
        self.assertEqual(pose.y, -75.5)
        self.assertEqual(pose.z, 20.0)
        self.assertEqual(pose.phi, 0.0)

    def test_instantiation_custom_phi(self) -> None:
        '''Verify custom phi value on initialization.'''
        pose = CartesianPose(x=100.0, y=50.0, z=10.0, phi=1.5708)
        self.assertEqual(pose.x, 100.0)
        self.assertEqual(pose.y, 50.0)
        self.assertEqual(pose.z, 10.0)
        self.assertEqual(pose.phi, 1.5708)

    def test_immutability(self) -> None:
        '''Verify frozen dataclass prevents mutation.'''
        pose = CartesianPose(x=0.0, y=0.0, z=0.0, phi=0.0)
        with self.assertRaises(FrozenInstanceError):
            pose.x = 25.0

    def test_equality(self) -> None:
        '''Verify value-object equality semantics.'''
        pose1 = CartesianPose(x=10.0, y=20.0, z=5.0, phi=0.5)
        pose2 = CartesianPose(x=10.0, y=20.0, z=5.0, phi=0.5)
        pose3 = CartesianPose(x=10.0, y=20.0, z=5.0, phi=1.0)
        self.assertEqual(pose1, pose2)
        self.assertNotEqual(pose1, pose3)


if __name__ == '__main__':
    main()
