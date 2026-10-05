# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_mutable_test.py
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
    Unit tests for ITrajectoryMutable protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_mutable import ITrajectoryMutable
from scaralang.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITrajectoryMutable(TestCase):
    '''
        Test cases for ITrajectoryMutable protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies TrajectoryPlan satisfies protocol.
                | test_mutation_methods - Verifies mutation operations via protocol interface.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete TrajectoryPlan satisfies ITrajectoryMutable protocol.'''
        plan = TrajectoryPlan()
        self.assertIsInstance(plan, ITrajectoryMutable)
        self.assertEqual(plan.name, 'trajectory_plan')

    def test_mutation_methods(self) -> None:
        '''Verifies mutation operations via ITrajectoryMutable interface.'''
        plan = TrajectoryPlan()
        mutable: ITrajectoryMutable = plan

        p1 = Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)
        p2 = Waypoint(x=30.0, y=40.0, z=0.0, speed=50.0)
        p_new = Waypoint(x=15.0, y=25.0, z=5.0, speed=60.0)

        mutable.add_point(p1)
        self.assertEqual(mutable.count, 1)

        mutable.insert_point(0, p2)
        self.assertEqual(mutable.count, 2)
        self.assertEqual(mutable.waypoints[0].x, 30.0)

        updated: bool = mutable.update_point(0, p_new)
        self.assertTrue(updated)
        self.assertEqual(mutable.waypoints[0].x, 15.0)

        removed: bool = mutable.remove_point(0)
        self.assertTrue(removed)
        self.assertEqual(mutable.count, 1)

        mutable.clear()
        self.assertEqual(mutable.count, 0)


if __name__ == '__main__':
    main()
