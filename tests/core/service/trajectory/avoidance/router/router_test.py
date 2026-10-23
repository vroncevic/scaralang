# -*- coding: UTF-8 -*-

'''
Module
    router_test.py
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
    Unit tests for SafeTrajectoryRouter class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.router.dependencies import RouterDependencies
from scaralang.core.service.trajectory.avoidance.router.router import SafeTrajectoryRouter
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSafeTrajectoryRouter(TestCase):
    '''
        Unit tests for SafeTrajectoryRouter unified trajectory routing.

        It defines:

            :methods:
                | test_plan_safe_trajectory_empty - Verifies empty waypoints return empty list.
                | test_plan_safe_trajectory_safe_path - Verifies direct path when no obstacle crossed.
                | test_plan_safe_trajectory_crossing_start - Verifies detour when initial lead-in crosses.
                | test_plan_safe_trajectory_crossing_intermediate - Verifies detour on intermediate segment.
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
        router_deps = RouterDependencies(
            validator=self._validator,
            bypass_planner=self._bypass_planner,
        )
        self._router = SafeTrajectoryRouter(dependencies=router_deps)

    def test_plan_safe_trajectory_empty(self) -> None:
        '''Verifies empty waypoints sequence returns empty list.'''
        start = Waypoint(x=150.0, y=0.0, z=10.0, phi=0.0, speed=50.0, name='', command='')
        result: list[Waypoint] = self._router.plan_safe_trajectory(start, [])
        self.assertEqual(result, [])

    def test_plan_safe_trajectory_safe_path(self) -> None:
        '''Verifies waypoints that do not cross dead zone are preserved directly.'''
        start = Waypoint(x=150.0, y=0.0, z=10.0, phi=0.0, speed=50.0, name='', command='')
        wp1 = Waypoint(x=150.0, y=50.0, z=10.0, phi=0.0, speed=50.0, name='P1', command='')
        wp2 = Waypoint(x=150.0, y=100.0, z=10.0, phi=0.0, speed=50.0, name='P2', command='')
        result: list[Waypoint] = self._router.plan_safe_trajectory(start, [wp1, wp2])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'P1')
        self.assertEqual(result[1].name, 'P2')

    def test_plan_safe_trajectory_crossing_start(self) -> None:
        '''Verifies detour arc inserted when segment from start to first waypoint crosses dead zone.'''
        start = Waypoint(x=-150.0, y=0.0, z=10.0, phi=0.0, speed=50.0, name='', command='')
        wp1 = Waypoint(x=150.0, y=0.0, z=10.0, phi=0.0, speed=50.0, name='TARGET', command='')
        result: list[Waypoint] = self._router.plan_safe_trajectory(start, [wp1])
        self.assertGreater(len(result), 1)
        self.assertEqual(result[-1].name, 'TARGET')
        self.assertAlmostEqual(result[-1].x, 150.0)
        self.assertAlmostEqual(result[-1].y, 0.0)

    def test_plan_safe_trajectory_crossing_intermediate(self) -> None:
        '''Verifies detour arc inserted when segment between waypoints crosses dead zone.'''
        start = Waypoint(x=150.0, y=50.0, z=10.0, phi=0.0, speed=50.0, name='', command='')
        wp1 = Waypoint(x=150.0, y=0.0, z=10.0, phi=0.0, speed=50.0, name='SAFE1', command='')
        wp2 = Waypoint(x=-150.0, y=0.0, z=10.0, phi=0.0, speed=50.0, name='OPPOSITE', command='')
        result: list[Waypoint] = self._router.plan_safe_trajectory(start, [wp1, wp2])
        self.assertGreater(len(result), 2)
        self.assertEqual(result[0].name, 'SAFE1')
        self.assertEqual(result[-1].name, 'OPPOSITE')

    def test_get_version(self) -> None:
        '''Verifies router get_version returns string.'''
        version: str = self._router.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
