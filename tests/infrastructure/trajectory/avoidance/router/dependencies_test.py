# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for DefaultRouterDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from math import pi
from unittest import TestCase, main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.infrastructure.trajectory.avoidance.router.dependencies import DefaultRouterDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultRouterDependencies(TestCase):
    '''
        Test cases for DefaultRouterDependencies container dataclass.

        It defines:

            :methods:
                | test_dependencies_defaults - Verifies default configuration values.
                | test_dependencies_custom - Verifies custom configuration values.
                | test_dependencies_immutability - Verifies frozen immutability of bundle.
    '''

    def test_dependencies_defaults(self) -> None:
        '''Verifies default parameters when constructing DefaultRouterDependencies.'''
        kinematic_bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        bundle = DefaultRouterDependencies(bounds=kinematic_bounds)
        self.assertIs(bundle.bounds, kinematic_bounds)
        self.assertAlmostEqual(bundle.safety_margin_mm, 5.0)
        self.assertAlmostEqual(bundle.angular_step_rad, pi / 12.0)

    def test_dependencies_custom(self) -> None:
        '''Verifies custom parameter initialization for router dependencies.'''
        kinematic_bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        bundle = DefaultRouterDependencies(
            bounds=kinematic_bounds,
            safety_margin_mm=8.5,
            angular_step_rad=0.25,
        )
        self.assertIs(bundle.bounds, kinematic_bounds)
        self.assertAlmostEqual(bundle.safety_margin_mm, 8.5)
        self.assertAlmostEqual(bundle.angular_step_rad, 0.25)

    def test_dependencies_immutability(self) -> None:
        '''Verifies frozen dataclass immutability for default router dependencies.'''
        kinematic_bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        bundle = DefaultRouterDependencies(bounds=kinematic_bounds)
        with self.assertRaises(FrozenInstanceError):
            bundle.safety_margin_mm = 6.0  # type: ignore[misc]


if __name__ == '__main__':
    main()
