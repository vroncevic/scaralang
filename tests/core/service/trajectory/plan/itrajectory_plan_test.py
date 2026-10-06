# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_plan_test.py
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
    Unit tests for ITrajectoryPlan protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scaralang.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITrajectoryPlan(TestCase):
    '''
        Test cases for ITrajectoryPlan composite protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies TrajectoryPlan satisfies protocol.
                | test_factory_conformance - Verifies factory returns ITrajectoryPlan instance.
                | test_protocol_operations - Verifies core operations via ITrajectoryPlan interface.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete TrajectoryPlan satisfies ITrajectoryPlan protocol.'''
        plan = TrajectoryPlan()
        self.assertIsInstance(plan, ITrajectoryPlan)
        self.assertEqual(plan.name, 'trajectory_plan')

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying ITrajectoryPlan protocol.'''
        plan = TrajectoryPlanFactory.create()
        self.assertIsInstance(plan, ITrajectoryPlan)
        self.assertEqual(plan.name, 'trajectory_plan')

    def test_protocol_operations(self) -> None:
        '''Verifies operations via ITrajectoryPlan interface.'''
        plan: ITrajectoryPlan = TrajectoryPlanFactory.create()
        self.assertEqual(plan.count, 0)

        plan.add_point(Waypoint(x=5.0, y=10.0, z=15.0, speed=25.0))
        self.assertEqual(plan.count, 1)
        self.assertEqual(plan.waypoints[0].z, 15.0)


if __name__ == '__main__':
    main()
