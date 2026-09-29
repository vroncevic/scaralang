# -*- coding: UTF-8 -*-

'''
Module
    cycle_time_calculator_test.py
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

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.metrics.cycle.cycle_time_calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.cycle.icycle_time_calculator import ICycleTimeCalculator
from scaralang.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCycleTimeCalculator(TestCase):
    '''Test suite verifying CycleTimeCalculator calculations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        calculator: CycleTimeCalculator = CycleTimeCalculator()
        self.assertTrue(isinstance(calculator, ICycleTimeCalculator))

    def test_segment_distance(self) -> None:
        '''Verifies 3D Euclidean segment distance calculation.'''
        calculator: CycleTimeCalculator = CycleTimeCalculator()
        p1: Waypoint = Waypoint(x=0.0, y=0.0, z=0.0, speed=100.0)
        p2: Waypoint = Waypoint(x=3.0, y=4.0, z=0.0, speed=100.0)
        dist: float = calculator.segment_distance(p1=p1, p2=p2)
        self.assertAlmostEqual(dist, 5.0, places=5)

    def test_calculate_distance_empty_and_single(self) -> None:
        '''Verifies distance calculation on empty and single waypoint plans.'''
        calculator: CycleTimeCalculator = CycleTimeCalculator()
        empty_plan: TrajectoryPlan = TrajectoryPlan()
        self.assertEqual(calculator.calculate_distance(plan=empty_plan), 0.0)

        single_plan: TrajectoryPlan = TrajectoryPlan()
        single_plan.add_point(point=Waypoint(x=10.0, y=20.0, z=5.0, speed=50.0))
        self.assertEqual(calculator.calculate_distance(plan=single_plan), 0.0)

    def test_calculate_distance_multiple_waypoints(self) -> None:
        '''Verifies cumulative path distance calculation.'''
        calculator: CycleTimeCalculator = CycleTimeCalculator()
        plan: TrajectoryPlan = TrajectoryPlan()
        plan.add_point(point=Waypoint(x=0.0, y=0.0, z=0.0, speed=100.0))
        plan.add_point(point=Waypoint(x=10.0, y=0.0, z=0.0, speed=100.0))
        plan.add_point(point=Waypoint(x=10.0, y=20.0, z=0.0, speed=100.0))
        self.assertAlmostEqual(calculator.calculate_distance(plan=plan), 30.0, places=5)

    def test_calculate_duration(self) -> None:
        '''Verifies total duration calculation in microseconds.'''
        calculator: CycleTimeCalculator = CycleTimeCalculator()
        plan: TrajectoryPlan = TrajectoryPlan()
        # 100mm move at 100mm/s -> 1.0s = 1_000_000us
        plan.add_point(point=Waypoint(x=0.0, y=0.0, z=0.0, speed=100.0))
        plan.add_point(point=Waypoint(x=100.0, y=0.0, z=0.0, speed=100.0))
        duration_us: int = calculator.calculate_duration(plan=plan)
        self.assertEqual(duration_us, 1000000)

    def test_calculate_duration_empty(self) -> None:
        '''Verifies duration calculation on empty plan.'''
        calculator: CycleTimeCalculator = CycleTimeCalculator()
        plan: TrajectoryPlan = TrajectoryPlan()
        self.assertEqual(calculator.calculate_duration(plan=plan), 0)


if __name__ == '__main__':
    main()
