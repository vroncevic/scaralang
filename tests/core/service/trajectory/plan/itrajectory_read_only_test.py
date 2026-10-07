# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_read_only_test.py
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
    Unit tests for ITrajectoryReadOnly protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scaralang.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITrajectoryReadOnly(TestCase):
    '''
        Test cases for ITrajectoryReadOnly protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies TrajectoryPlan satisfies protocol.
                | test_read_only_properties - Verifies read-only properties inspect waypoints.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete TrajectoryPlan satisfies ITrajectoryReadOnly protocol.'''
        plan = TrajectoryPlan()
        self.assertIsInstance(plan, ITrajectoryReadOnly)
        self.assertEqual(plan.name, 'trajectory_plan')

    def test_read_only_properties(self) -> None:
        '''Verifies waypoints and count properties via ITrajectoryReadOnly interface.'''
        plan = TrajectoryPlan()
        read_only: ITrajectoryReadOnly = plan
        self.assertEqual(read_only.count, 0)
        self.assertEqual(len(read_only.waypoints), 0)

        plan.add_point(Waypoint(x=10.0, y=20.0, z=0.0, speed=100.0))
        self.assertEqual(read_only.count, 1)
        self.assertEqual(read_only.waypoints[0].x, 10.0)


if __name__ == '__main__':
    main()
