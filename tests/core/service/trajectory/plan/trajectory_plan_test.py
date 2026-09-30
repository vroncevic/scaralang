# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_test.py
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
    Unit tests for TrajectoryPlan domain service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_mutable import ITrajectoryMutable
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scaralang.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scaralang.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryPlan(TestCase):
    '''
        Test cases for TrajectoryPlan entity.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_name_property - Verifies name property returns expected identifier.
                | test_add_and_count - Tests adding waypoints and count property.
                | test_insert_point - Tests inserting a point at specific index.
                | test_update_and_remove - Tests point modification and removal.
                | test_clear - Tests clearing all waypoints.
                | test_protocol_conformance - Verifies structural protocol compliance.
                | test_factory_create - Verifies factory creation.
    '''

    def setUp(self) -> None:
        '''Initializes test fixtures.'''
        self.plan: TrajectoryPlan = TrajectoryPlan()

    def test_name_property(self) -> None:
        '''Verifies name property returns correct identifier.'''
        self.assertEqual(self.plan.name, 'trajectory_plan')

    def test_add_and_count(self) -> None:
        '''Tests adding waypoints and count property.'''
        self.assertEqual(self.plan.count, 0)
        p1 = Waypoint(x=0.0, y=0.0, z=20.0, phi=0.0, speed=40.0)
        p2 = Waypoint(x=40.0, y=0.0, z=20.0, phi=0.0, speed=40.0)
        p3 = Waypoint(x=40.0, y=30.0, z=20.0, phi=0.0, speed=40.0)

        self.plan.add_point(p1)
        self.plan.add_point(p2)
        self.plan.add_point(p3)

        self.assertEqual(self.plan.count, 3)
        self.assertEqual(len(self.plan.waypoints), 3)

    def test_insert_point(self) -> None:
        '''Tests inserting a waypoint at a specific index.'''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        p2 = Waypoint(x=30.0, y=30.0, z=0.0, phi=0.0, speed=10.0)
        p_mid = Waypoint(x=20.0, y=20.0, z=0.0, phi=0.0, speed=10.0)

        self.plan.add_point(p1)
        self.plan.add_point(p2)
        self.plan.insert_point(1, p_mid)

        self.assertEqual(self.plan.count, 3)
        self.assertEqual(self.plan.waypoints[1].x, 20.0)

    def test_update_and_remove(self) -> None:
        '''Tests updating and removing waypoint elements.'''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        p2 = Waypoint(x=20.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.plan.set_waypoints([p1, p2])

        p1_mod = Waypoint(x=15.0, y=15.0, z=0.0, phi=0.0, speed=10.0)
        updated = self.plan.update_point(0, p1_mod)
        self.assertTrue(updated)
        self.assertEqual(self.plan.waypoints[0].x, 15.0)

        invalid_update = self.plan.update_point(99, p1_mod)
        self.assertFalse(invalid_update)

        removed = self.plan.remove_point(0)
        self.assertTrue(removed)
        self.assertEqual(self.plan.count, 1)
        self.assertEqual(self.plan.waypoints[0].x, 20.0)

        invalid_remove = self.plan.remove_point(99)
        self.assertFalse(invalid_remove)

    def test_clear(self) -> None:
        '''Tests clearing all waypoints.'''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        self.plan.add_point(p1)
        self.plan.clear()
        self.assertEqual(self.plan.count, 0)

    def test_protocol_conformance(self) -> None:
        '''Verifies structural protocol compliance of TrajectoryPlan.'''
        self.assertIsInstance(self.plan, ITrajectoryPlan)
        self.assertIsInstance(self.plan, ITrajectoryMutable)
        self.assertIsInstance(self.plan, ITrajectoryReadOnly)

    def test_factory_create(self) -> None:
        '''Verifies TrajectoryPlanFactory instantiation.'''
        plan = TrajectoryPlanFactory.create()
        self.assertIsInstance(plan, TrajectoryPlan)
        self.assertIsInstance(plan, ITrajectoryPlan)


if __name__ == '__main__':
    main()
