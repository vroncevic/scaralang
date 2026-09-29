# -*- coding: UTF-8 -*-

'''
Module
    cycle_time_calculator.py
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
    Defines CycleTimeCalculator computing motion duration and 3D path distance.
'''

from __future__ import annotations

from collections.abc import Sequence
from math import sqrt

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CycleTimeCalculator:
    '''
        Calculates cumulative trajectory execution duration and path distance.

        It defines:

            :attributes:
                | name - Identifier name of the cycle time calculator.
            :methods:
                | __init__ - Initializes CycleTimeCalculator instance.
                | calculate_duration - Computes cumulative execution duration in microseconds.
                | calculate_distance - Computes total 3D Cartesian distance along path.
                | segment_distance - Computes Euclidean 3D distance between two waypoints.
    '''

    def __init__(self) -> None:
        '''
            Initializes CycleTimeCalculator instance.
        '''

    @property
    def name(self) -> str:
        '''
            Gets the calculator identifier name.

            :return: Calculator name string.
        '''
        return 'cycle_time_calculator'

    def segment_distance(self, *, p1: Waypoint, p2: Waypoint) -> float:
        '''
            Computes 3D Euclidean distance between two waypoints.

            :param p1: Starting waypoint.
            :param p2: Ending waypoint.
            :return: 3D distance in millimeters.
        '''
        dx: float = p2.x - p1.x
        dy: float = p2.y - p1.y
        dz: float = p2.z - p1.z

        return sqrt(dx * dx + dy * dy + dz * dz)

    def calculate_distance(self, *, plan: ITrajectoryPlan) -> float:
        '''
            Computes total 3D Cartesian distance along trajectory path in millimeters.

            :param plan: Trajectory plan containing waypoints.
            :return: Cumulative distance in millimeters.
        '''
        waypoints: Sequence[Waypoint] = plan.waypoints

        if len(waypoints) < 2:
            return 0.0

        total_mm: float = 0.0

        for i in range(len(waypoints) - 1):
            total_mm += self.segment_distance(p1=waypoints[i], p2=waypoints[i + 1])

        return total_mm

    def calculate_duration(self, *, plan: ITrajectoryPlan) -> int:
        '''
            Computes cumulative execution duration in microseconds across all waypoints in plan.

            :param plan: Trajectory plan containing waypoints.
            :return: Total duration in microseconds.
        '''
        waypoints: Sequence[Waypoint] = plan.waypoints

        if len(waypoints) < 2:
            return 0

        total_sec: float = 0.0

        for i in range(len(waypoints) - 1):
            dist: float = self.segment_distance(p1=waypoints[i], p2=waypoints[i + 1])
            spd: float = max(1.0, waypoints[i + 1].speed)
            total_sec += dist / spd

        return int(total_sec * 1000000.0)
