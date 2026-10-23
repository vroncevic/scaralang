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
    Unit tests for DefaultValidationFactory infrastructure factory.
'''

from __future__ import annotations

from math import cos, sqrt
from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.avoidance.validation.provides import ValidationProvides
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultValidationFactory(TestCase):
    '''
        Test cases for DefaultValidationFactory creation logic.

        It defines:

            :methods:
                | test_create - Verifies factory builds ValidationProvides from bounds.
                | test_get_version - Verifies factory version string representation.
    '''

    def test_create(self) -> None:
        '''Verifies factory builds ValidationProvides respecting bounds deadzone override.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dependencies = DefaultValidationDependencies(bounds=bounds)
        provides: ValidationProvides = DefaultValidationFactory.create(dependencies=dependencies)
        self.assertIsInstance(provides, ValidationProvides)

        l1: float = bounds.links.l1
        l2: float = bounds.links.l2
        j2_max: float = bounds.joints.j2_max_rad
        kinematic_r_sq: float = l1 * l1 + l2 * l2 + 2.0 * l1 * l2 * cos(j2_max)
        kinematic_r_min: float = sqrt(max(0.0, kinematic_r_sq))
        expected_r_min: float = max(
            kinematic_r_min,
            abs(l1 - l2),
            bounds.singularity.deadzone_r_min,
        )
        self.assertEqual(provides.validator.get_dead_zone_radius(), expected_r_min)

    def test_get_version(self) -> None:
        '''Verifies factory version getter.'''
        self.assertIsInstance(DefaultValidationFactory.get_version(), str)
        self.assertTrue(len(DefaultValidationFactory.get_version()) > 0)


if __name__ == '__main__':
    main()
