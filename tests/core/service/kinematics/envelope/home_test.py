# -*- coding: UTF-8 -*-

'''
Module
    home_test.py
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
    Unit tests for HomePoseCalculator reference pose generation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.envelope.home import HomePoseCalculator
from scaralang.core.service.kinematics.envelope.ihome import IHomePoseCalculator
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHomePoseCalculator(TestCase):
    '''
        Validates HomePoseCalculator canonical home pose calculation and protocol conformance.

        It defines:

            :methods:
                | setUp - Initializes bounds and calculator instance.
                | test_structural_conformance - Verifies conformance to IHomePoseCalculator.
                | test_calculate_home_pose_default - Verifies default home pose calculation.
                | test_calculate_home_pose_custom - Verifies customized home pose parameters.
                | test_get_version - Verifies version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes standard bounds and HomePoseCalculator instance.
        '''
        self.bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        self.calculator: HomePoseCalculator = HomePoseCalculator(bounds=self.bounds)

    def test_structural_conformance(self) -> None:
        '''
            Verifies HomePoseCalculator conforms structurally to IHomePoseCalculator.
        '''
        self.assertIsInstance(self.calculator, IHomePoseCalculator)

    def test_calculate_home_pose_default(self) -> None:
        '''
            Verifies default canonical home Cartesian 4-DOF pose.
        '''
        home: CartesianPose = self.calculator.calculate_home_pose()
        expected_reach: float = (self.bounds.links.l1 + self.bounds.links.l2) * 0.65
        expected_z: float = self.bounds.vertical.z_min + 20.0

        self.assertEqual(home.x, expected_reach)
        self.assertEqual(home.y, 0.0)
        self.assertEqual(home.z, expected_z)
        self.assertEqual(home.phi, 0.0)

    def test_calculate_home_pose_custom(self) -> None:
        '''
            Verifies customized home Cartesian 4-DOF pose calculation.
        '''
        home: CartesianPose = self.calculator.calculate_home_pose(
            reach_ratio=0.5,
            z_offset_mm=10.0,
            phi=1.57,
        )
        expected_reach: float = (self.bounds.links.l1 + self.bounds.links.l2) * 0.5
        expected_z: float = self.bounds.vertical.z_min + 10.0

        self.assertEqual(home.x, expected_reach)
        self.assertEqual(home.y, 0.0)
        self.assertEqual(home.z, expected_z)
        self.assertEqual(home.phi, 1.57)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string.
        '''
        self.assertEqual(self.calculator.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
