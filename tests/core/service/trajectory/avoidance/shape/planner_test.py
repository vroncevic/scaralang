# -*- coding: UTF-8 -*-

'''
Module
    planner_test.py
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
    Unit tests for AvoidanceShapePlanner class.
'''

from __future__ import annotations

from math import sqrt
from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.shape.planner import AvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAvoidanceShapePlanner(TestCase):
    '''
        Unit tests for AvoidanceShapePlanner shape trajectory routing.

        It defines:

            :methods:
                | test_plan_contour_empty - Verifies empty sequence returns empty list.
                | test_plan_contour_single_point - Verifies single point returns one waypoint.
                | test_plan_contour_line_safe - Verifies safe segment returns direct start and end.
                | test_plan_contour_line_crossing - Verifies crossing line routes detour.
                | test_plan_contour_rectangle_safe - Verifies safe rectangle returns 5 vertices.
                | test_plan_contour_rectangle_crossing - Verifies crossing rectangle routes detour.
                | test_plan_contour_open - Verifies open polygon without closing vertex.
                | test_plan_contour_already_closed - Verifies polygon already ending with start vertex.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''Sets up test fixtures with 86mm dead zone and 5mm safe margin.'''
        self._dead_zone_r: float = 86.0
        self._safe_margin: float = 5.0
        self._validator: IDeadZoneValidator = ValidationFactory.create(
            dead_zone_radius=self._dead_zone_r,
        ).validator
        calculator = ArcFactory.create().calculator
        deps = BypassDependencies(
            validator=self._validator,
            calculator=calculator,
            safety_margin_mm=self._safe_margin,
        )
        self._bypass_planner: IDeadZoneBypassPlanner = (
            BypassFactory.create(dependencies=deps).planner
        )
        shape_deps = ShapeDependencies(
            validator=self._validator,
            bypass_planner=self._bypass_planner,
        )
        self._planner = AvoidanceShapePlanner(dependencies=shape_deps)

    def test_plan_contour_empty(self) -> None:
        '''Verifies empty point sequence returns empty list.'''
        waypoints: list[Waypoint] = self._planner.plan_contour(
            (),
            z=15.0,
            speed=50.0,
        )
        self.assertEqual(waypoints, [])

    def test_plan_contour_single_point(self) -> None:
        '''Verifies single point sequence returns list with one waypoint.'''
        pt = Point2D(x=120.0, y=80.0)
        waypoints: list[Waypoint] = self._planner.plan_contour(
            (pt,),
            z=15.0,
            speed=50.0,
        )
        self.assertEqual(len(waypoints), 1)
        self.assertAlmostEqual(waypoints[0].x, 120.0)
        self.assertAlmostEqual(waypoints[0].y, 80.0)
        self.assertAlmostEqual(waypoints[0].z, 15.0)
        self.assertAlmostEqual(waypoints[0].speed, 50.0)

    def test_plan_contour_line_safe(self) -> None:
        '''Verifies non-intersecting open segment produces exactly two boundary waypoints.'''
        pts = (Point2D(x=100.0, y=100.0), Point2D(x=150.0, y=100.0))
        waypoints: list[Waypoint] = self._planner.plan_contour(
            pts,
            z=20.0,
            speed=60.0,
            closed=False,
        )
        self.assertEqual(len(waypoints), 2)
        self.assertAlmostEqual(waypoints[0].x, 100.0)
        self.assertAlmostEqual(waypoints[1].x, 150.0)

    def test_plan_contour_line_crossing(self) -> None:
        '''Verifies crossing line inserts detour waypoints clearing safe radius.'''
        pts = (Point2D(x=-120.0, y=0.0), Point2D(x=120.0, y=0.0))
        waypoints: list[Waypoint] = self._planner.plan_contour(
            pts,
            z=10.0,
            speed=40.0,
            closed=False,
        )
        self.assertGreater(len(waypoints), 2)
        for wp in waypoints:
            r = sqrt(wp.x * wp.x + wp.y * wp.y)
            self.assertGreaterEqual(r, self._dead_zone_r - 0.01)

    def test_plan_contour_rectangle_safe(self) -> None:
        '''Verifies rectangle outside dead zone returns standard 5 corner vertices.'''
        pts = (
            Point2D(x=100.0, y=100.0),
            Point2D(x=150.0, y=100.0),
            Point2D(x=150.0, y=150.0),
            Point2D(x=100.0, y=150.0),
        )
        waypoints: list[Waypoint] = self._planner.plan_contour(
            pts,
            z=25.0,
            speed=50.0,
            closed=True,
        )
        self.assertEqual(len(waypoints), 5)
        self.assertAlmostEqual(waypoints[0].x, waypoints[-1].x)
        self.assertAlmostEqual(waypoints[0].y, waypoints[-1].y)

    def test_plan_contour_rectangle_crossing(self) -> None:
        '''Verifies rectangle traversing dead zone routes around the obstacle.'''
        pts = (
            Point2D(x=-105.0, y=75.0),
            Point2D(x=105.0, y=75.0),
            Point2D(x=105.0, y=-75.0),
            Point2D(x=-105.0, y=-75.0),
        )
        waypoints: list[Waypoint] = self._planner.plan_contour(
            pts,
            z=20.0,
            speed=50.0,
            closed=True,
        )
        self.assertGreater(len(waypoints), 5)
        for wp in waypoints:
            r = sqrt(wp.x * wp.x + wp.y * wp.y)
            self.assertGreaterEqual(r, self._dead_zone_r - 0.01)

    def test_plan_contour_open(self) -> None:
        '''Verifies open polygon plans sequentially without adding closing vertex.'''
        pts = (
            Point2D(x=100.0, y=100.0),
            Point2D(x=120.0, y=110.0),
            Point2D(x=140.0, y=90.0),
        )
        waypoints: list[Waypoint] = self._planner.plan_contour(
            pts,
            z=10.0,
            speed=30.0,
            closed=False,
        )
        self.assertEqual(len(waypoints), 3)

    def test_plan_contour_already_closed(self) -> None:
        '''Verifies polygon already ending with start vertex does not duplicate end.'''
        pts = (
            Point2D(x=100.0, y=100.0),
            Point2D(x=120.0, y=100.0),
            Point2D(x=120.0, y=120.0),
            Point2D(x=100.0, y=100.0),
        )
        waypoints: list[Waypoint] = self._planner.plan_contour(
            pts,
            z=10.0,
            speed=30.0,
            closed=True,
        )
        self.assertEqual(len(waypoints), 4)

    def test_get_version(self) -> None:
        '''Verifies get_version returns semantic version string.'''
        version: str = self._planner.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
