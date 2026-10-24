# -*- coding: UTF-8 -*-

'''
Module
    bounds_test.py
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
    Unit tests for ScaraBounds kinematics domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BoundsTest(TestCase):
    '''
        Unit tests validating ScaraBounds purity, immutability, and attribute values.

        It defines:

            :methods:
                | test_instantiation_and_attributes - Verifies field values on initialization.
                | test_frozen_immutability - Verifies frozen dataclass prevents mutation.
    '''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verify proper initialization and access of ScaraBounds fields.

            :exceptions: None.
        '''
        bounds = ScaraBounds(
            links=LinkDimensions(l1=200.0, l2=150.0),
            vertical=VerticalBounds(z_min=0.0, z_max=100.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=500.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=1000.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.5,
                j1_max_rad=2.5,
                j2_min_rad=-2.8,
                j2_max_rad=2.8,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=10.0,
                singularity_theta2_min_rad=0.05,
                deadzone_r_min=60.0,
            ),
        )
        self.assertEqual(bounds.links.l1, 200.0)
        self.assertEqual(bounds.links.l2, 150.0)
        self.assertEqual(bounds.vertical.z_min, 0.0)
        self.assertEqual(bounds.vertical.z_max, 100.0)
        self.assertEqual(bounds.speeds.min_speed, 1.0)
        self.assertEqual(bounds.speeds.max_speed, 500.0)
        self.assertEqual(bounds.speeds.default_speed, 50.0)
        self.assertEqual(bounds.speeds.default_accel, 100.0)
        self.assertEqual(bounds.speeds.max_accel, 1000.0)
        self.assertEqual(bounds.joints.j1_min_rad, -2.5)
        self.assertEqual(bounds.joints.j1_max_rad, 2.5)
        self.assertEqual(bounds.joints.j2_min_rad, -2.8)
        self.assertEqual(bounds.joints.j2_max_rad, 2.8)
        self.assertEqual(bounds.singularity.singularity_outer_margin_mm, 5.0)
        self.assertEqual(bounds.singularity.singularity_inner_margin_mm, 10.0)
        self.assertEqual(bounds.singularity.singularity_theta2_min_rad, 0.05)
        self.assertEqual(bounds.singularity.deadzone_r_min, 60.0)

    def test_frozen_immutability(self) -> None:
        '''
            Verify that modifying attributes on ScaraBounds raises FrozenInstanceError.

            :exceptions: None.
        '''
        bounds = ScaraBounds(
            links=LinkDimensions(l1=200.0, l2=150.0),
            vertical=VerticalBounds(z_min=0.0, z_max=100.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=500.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=1000.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.5,
                j1_max_rad=2.5,
                j2_min_rad=-2.8,
                j2_max_rad=2.8,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=10.0,
                singularity_theta2_min_rad=0.05,
                deadzone_r_min=60.0,
            ),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(bounds, 'links', LinkDimensions(l1=300.0, l2=150.0))


if __name__ == '__main__':
    main()
