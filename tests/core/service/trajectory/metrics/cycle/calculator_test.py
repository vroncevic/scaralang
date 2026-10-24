# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for CycleTimeCalculator service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.metrics.cycle.calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCycleTimeCalculator(TestCase):
    '''Test suite verifying calculations performed by CycleTimeCalculator.'''

    def test_name_property(self) -> None:
        '''Verifies name property returns expected identifier string.'''
        calc = CycleTimeCalculator()
        self.assertEqual(calc.name, 'cycle_time_calculator')

    def test_segment_distance(self) -> None:
        '''Verifies 3D Euclidean segment distance calculation between two waypoints.'''
        calc = CycleTimeCalculator()
        start = Waypoint(x=0.0, y=0.0, z=0.0, phi=0.0, speed=100.0, name='', command='')
        end = Waypoint(x=3.0, y=4.0, z=0.0, phi=0.0, speed=100.0, name='', command='')
        self.assertAlmostEqual(calc.segment_distance(p1=start, p2=end), 5.0, places=5)

    def test_calculate_distance_empty_and_single(self) -> None:
        '''Verifies distance calculation on empty and single waypoint plans.'''
        calc = CycleTimeCalculator()
        empty_plan = TrajectoryPlan(waypoints=())
        self.assertEqual(calc.calculate_distance(plan=empty_plan), 0.0)

        single_pt_plan = TrajectoryPlan(
            waypoints=[
                Waypoint(
                    x=10.0,
                    y=20.0,
                    z=5.0,
                    phi=0.0,
                    speed=50.0,
                    name='',
                    command='',
                )
            ]
        )
        self.assertEqual(calc.calculate_distance(plan=single_pt_plan), 0.0)

    def test_calculate_distance_multiple_waypoints(self) -> None:
        '''Verifies cumulative path distance calculation across sequential points.'''
        calc = CycleTimeCalculator()
        multi_plan = TrajectoryPlan(
            waypoints=[
                Waypoint(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
                Waypoint(
                    x=10.0,
                    y=0.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
                Waypoint(
                    x=10.0,
                    y=20.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
            ]
        )
        self.assertAlmostEqual(calc.calculate_distance(plan=multi_plan), 30.0, places=5)

    def test_calculate_duration_with_motion(self) -> None:
        '''Verifies total duration calculation in microseconds for moving segments.'''
        calc = CycleTimeCalculator()
        # 100mm move at 100mm/s -> 1.0s = 1_000_000us
        timed_plan = TrajectoryPlan(
            waypoints=[
                Waypoint(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
                Waypoint(
                    x=100.0,
                    y=0.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
            ]
        )
        duration_us = calc.calculate_duration(plan=timed_plan)
        self.assertEqual(duration_us, 1000000)

    def test_calculate_duration_empty(self) -> None:
        '''Verifies duration calculation on empty plan produces 0 microseconds.'''
        calc = CycleTimeCalculator()
        blank_plan = TrajectoryPlan(waypoints=())
        self.assertEqual(calc.calculate_duration(plan=blank_plan), 0)


if __name__ == '__main__':
    main()
