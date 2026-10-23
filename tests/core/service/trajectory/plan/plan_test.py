# -*- coding: UTF-8 -*-

'''
Module
    plan_test.py
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
    Unit tests for package-scoped TrajectoryPlan aggregate.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.factory import PlanFactory
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.iread_only import ITrajectoryReadOnly
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
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
                | test_waypoints_and_count - Tests waypoints and count properties.
                | test_get_version - Tests get_version reporting.
                | test_protocol_conformance - Verifies structural protocol compliance.
                | test_factory_create - Verifies factory creation.
    '''

    def setUp(self) -> None:
        '''Initializes test fixtures.'''
        self.plan: TrajectoryPlan = TrajectoryPlan(waypoints=())

    def test_name_property(self) -> None:
        '''Verifies name property returns correct identifier.'''
        self.assertEqual(self.plan.name, 'trajectory_plan')

    def test_waypoints_and_count(self) -> None:
        '''Tests waypoints and count properties with sequence initialization.'''
        p1 = Waypoint(x=0.0, y=0.0, z=20.0, phi=0.0, speed=40.0, name='', command='')
        p2 = Waypoint(x=40.0, y=0.0, z=20.0, phi=0.0, speed=40.0, name='', command='')
        p3 = Waypoint(x=40.0, y=30.0, z=20.0, phi=0.0, speed=40.0, name='', command='')

        plan = TrajectoryPlan(waypoints=[p1, p2, p3])
        self.assertEqual(plan.count, 3)
        self.assertEqual(len(plan.waypoints), 3)
        self.assertEqual(plan.waypoints[0].z, 20.0)
        self.assertEqual(plan.waypoints[2].y, 30.0)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.plan.get_version(), str)
        self.assertEqual(self.plan.get_version(), '1.1.0')

    def test_protocol_conformance(self) -> None:
        '''Verifies structural protocol compliance of TrajectoryPlan.'''
        self.assertIsInstance(self.plan, ITrajectoryPlan)
        self.assertIsInstance(self.plan, ITrajectoryReadOnly)

    def test_factory_create(self) -> None:
        '''Verifies PlanFactory plan creation.'''
        plan = PlanFactory.create().plan
        self.assertIsInstance(plan, TrajectoryPlan)
        self.assertIsInstance(plan, ITrajectoryPlan)


if __name__ == '__main__':
    main()
