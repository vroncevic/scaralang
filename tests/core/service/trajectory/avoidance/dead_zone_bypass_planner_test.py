# -*- coding: UTF-8 -*-

'''
Module
    dead_zone_bypass_planner_test.py
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
    Unit tests for DeadZoneBypassPlanner service.
'''

from __future__ import annotations

from math import hypot
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.dead_zone_bypass_planner import DeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.dead_zone_validator import DeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDeadZoneBypassPlanner(TestCase):
    '''
        Test cases for DeadZoneBypassPlanner obstacle detour generation.

        It defines:

            :methods:
                | setUp - Initializes DeadZoneBypassPlanner with validator.
                | test_plan_bypass_safe_direct - Verifies direct path when no traversal occurs.
                | test_plan_bypass_crossing_ccw - Verifies CCW bypass arc generation.
                | test_plan_bypass_crossing_cw - Verifies CW bypass arc generation.
                | test_plan_bypass_clearance - Verifies all generated points clear the dead zone.
                | test_get_safe_radius - Verifies safe radius calculation.
                | test_get_version - Verifies version string accessor.
    '''

    def setUp(self) -> None:
        '''Initializes planner with 86.0 mm dead zone and 5.0 mm safety margin.'''
        self.validator = DeadZoneValidator(dead_zone_radius=86.0)
        self.planner = DeadZoneBypassPlanner(
            validator=self.validator,
            safety_margin_mm=5.0,
        )

    def test_plan_bypass_safe_direct(self) -> None:
        '''Verifies segment not traversing dead zone returns destination directly.'''
        p1 = Point2D(x=120.0, y=100.0)
        p2 = Point2D(x=150.0, y=120.0)
        waypoints: list[Waypoint] = self.planner.plan_bypass(
            start_pt=p1,
            end_pt=p2,
            z=15.0,
            speed=50.0,
        )
        self.assertEqual(len(waypoints), 1)
        self.assertAlmostEqual(waypoints[0].x, 150.0)
        self.assertAlmostEqual(waypoints[0].y, 120.0)
        self.assertEqual(waypoints[0].z, 15.0)
        self.assertEqual(waypoints[0].speed, 50.0)

    def test_plan_bypass_crossing_ccw(self) -> None:
        '''Verifies detour generation when segment crosses center in CCW angular direction.'''
        p1 = Point2D(x=-120.0, y=10.0)
        p2 = Point2D(x=120.0, y=10.0)
        waypoints: list[Waypoint] = self.planner.plan_bypass(
            start_pt=p1,
            end_pt=p2,
            z=10.0,
            speed=80.0,
        )
        self.assertGreater(len(waypoints), 2)
        final_wp = waypoints[-1]
        self.assertAlmostEqual(final_wp.x, 120.0)
        self.assertAlmostEqual(final_wp.y, 10.0)
        self.assertEqual(final_wp.z, 10.0)
        self.assertEqual(final_wp.speed, 80.0)

    def test_plan_bypass_crossing_cw(self) -> None:
        '''Verifies detour generation when segment crosses center in CW angular direction.'''
        p1 = Point2D(x=120.0, y=10.0)
        p2 = Point2D(x=-120.0, y=10.0)
        waypoints: list[Waypoint] = self.planner.plan_bypass(
            start_pt=p1,
            end_pt=p2,
            z=25.0,
            speed=100.0,
        )
        self.assertGreater(len(waypoints), 2)
        final_wp = waypoints[-1]
        self.assertAlmostEqual(final_wp.x, -120.0)
        self.assertAlmostEqual(final_wp.y, 10.0)

    def test_plan_bypass_clearance(self) -> None:
        '''Verifies all detour intermediate points remain strictly outside dead zone.'''
        p1 = Point2D(x=-140.0, y=0.0)
        p2 = Point2D(x=140.0, y=0.0)
        waypoints: list[Waypoint] = self.planner.plan_bypass(
            start_pt=p1,
            end_pt=p2,
            z=0.0,
            speed=60.0,
        )
        for wp in waypoints:
            radial_dist: float = hypot(wp.x, wp.y)
            self.assertGreaterEqual(
                radial_dist,
                86.0,
                f'Waypoint ({wp.x}, {wp.y}) violated dead zone clearance!',
            )

    def test_get_safe_radius(self) -> None:
        '''Verifies safe radius includes safety margin over dead zone radius.'''
        self.assertEqual(self.planner.get_safe_radius(), 91.0)

    def test_get_version(self) -> None:
        '''Verifies version string accessor returns valid representation.'''
        self.assertIsInstance(self.planner.get_version(), str)
        self.assertTrue(len(self.planner.get_version()) > 0)


if __name__ == '__main__':
    main()
