# -*- coding: UTF-8 -*-

'''
Module
    icycle_time_calculator.py
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
    Defines structural interface protocol for trajectory cycle-time and distance calculation.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICycleTimeCalculator(Protocol):
    '''
        Structural interface protocol for trajectory cycle duration and path distance calculations.

        It defines:

            :attributes:
                | name - Identifier name of the cycle time calculator.
            :methods:
                | calculate_duration - Computes cumulative execution duration in microseconds.
                | calculate_distance - Computes total 3D Cartesian distance along the path.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the calculator identifier name.

            :return: Calculator name string.
        '''

    def calculate_duration(self, *, plan: ITrajectoryPlan) -> int:
        '''
            Computes cumulative execution duration in microseconds across all waypoints in plan.

            :param plan: Trajectory plan containing waypoints.
            :return: Total duration in microseconds.
        '''

    def calculate_distance(self, *, plan: ITrajectoryPlan) -> float:
        '''
            Computes total 3D Cartesian distance along the trajectory path in millimeters.

            :param plan: Trajectory plan containing waypoints.
            :return: Cumulative distance in mm.
        '''
