# -*- coding: UTF-8 -*-

'''
Module
    dead_zone_bypass_planner_factory_test.py
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
    Unit tests for DeadZoneBypassPlannerFactory factory.
'''

from __future__ import annotations

from math import cos
from math import sqrt
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.avoidance.dead_zone_bypass_planner_factory import DeadZoneBypassPlannerFactory
from scaralang.core.service.trajectory.avoidance.dead_zone_validator import DeadZoneValidator
from scaralang.core.service.trajectory.avoidance.idead_zone_bypass_planner import IDeadZoneBypassPlanner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDeadZoneBypassPlannerFactory(TestCase):
    '''
        Test cases for DeadZoneBypassPlannerFactory creation methods.

        It defines:

            :methods:
                | test_create_with_validator - Verifies creation with injected validator.
                | test_create_from_bounds - Verifies creation directly from ScaraBounds model.
                | test_get_version - Verifies factory version string accessor.
    '''

    def test_create_with_validator(self) -> None:
        '''Verifies factory builds IDeadZoneBypassPlanner using injected validator.'''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        planner: IDeadZoneBypassPlanner = DeadZoneBypassPlannerFactory.create(
            validator=validator,
            safety_margin_mm=10.0,
        )
        self.assertIsInstance(planner, IDeadZoneBypassPlanner)
        self.assertEqual(planner.get_safe_radius(), 96.0)

    def test_create_from_bounds(self) -> None:
        '''Verifies factory builds IDeadZoneBypassPlanner from ScaraBounds model.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        planner: IDeadZoneBypassPlanner = DeadZoneBypassPlannerFactory.create_from_bounds(
            bounds=bounds,
            safety_margin_mm=4.0,
        )
        self.assertIsInstance(planner, IDeadZoneBypassPlanner)
        l1: float = bounds.links.l1
        l2: float = bounds.links.l2
        j2_max: float = bounds.joints.j2_max_rad
        kinematic_r_sq: float = l1 * l1 + l2 * l2 + 2.0 * l1 * l2 * cos(j2_max)
        kinematic_r_min: float = sqrt(max(0.0, kinematic_r_sq))
        expected_deadzone: float = max(
            kinematic_r_min,
            abs(l1 - l2),
            bounds.singularity.deadzone_r_min,
        )
        self.assertEqual(planner.get_safe_radius(), expected_deadzone + 4.0)

    def test_get_version(self) -> None:
        '''Verifies factory version getter.'''
        self.assertIsInstance(DeadZoneBypassPlannerFactory.get_version(), str)
        self.assertTrue(len(DeadZoneBypassPlannerFactory.get_version()) > 0)


if __name__ == '__main__':
    main()
