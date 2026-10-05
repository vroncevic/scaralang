# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan.py
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
    Implementation of TrajectoryPlan aggregate managing compiled motion waypoints.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPlan:
    '''
        TrajectoryPlan implementation holding compiled waypoints.

        It defines:

            :attributes:
                | name - Identifier name of the trajectory plan.
                | _waypoints - Mutable list of compiled Waypoint entities.
            :methods:
                | __init__ - Initializes empty trajectory plan.
                | waypoints - Returns read-only view of waypoints.
                | count - Returns total number of points in plan.
                | add_point - Appends a new waypoint to the plan.
                | insert_point - Inserts a waypoint at a specific index.
                | update_point - Replaces waypoint at index.
                | remove_point - Removes waypoint at index.
                | clear - Clears all waypoints.
                | set_waypoints - Replaces all waypoints with a new sequence.
    '''

    _waypoints: list[Waypoint]

    def __init__(self) -> None:
        '''
            Initializes an empty trajectory plan.

            :exceptions: None.
        '''
        self._waypoints = []

    @property
    def name(self) -> str:
        '''
            Gets the trajectory plan identifier name.

            :return: Trajectory plan name string.
        '''
        return 'trajectory_plan'

    @property
    def waypoints(self) -> Sequence[Waypoint]:
        '''
            Returns read-only view of waypoints.

            :return: Tuple of Waypoint instances.
            :exceptions: None.
        '''
        return tuple(self._waypoints)

    @property
    def count(self) -> int:
        '''
            Returns total number of points in plan.

            :return: Number of waypoints.
            :exceptions: None.
        '''
        return len(self._waypoints)

    def add_point(self, point: Waypoint) -> None:
        '''
            Appends a new point to the plan.

            :param point: Waypoint entity to add.
            :exceptions: None.
        '''
        self._waypoints.append(point)

    def insert_point(self, index: int, point: Waypoint) -> None:
        '''
            Inserts a point at a specific index.

            :param index: Target index.
            :param point: Waypoint entity to insert.
            :exceptions: None.
        '''
        self._waypoints.insert(index, point)

    def update_point(self, index: int, new_point: Waypoint) -> bool:
        '''
            Updates an existing point at a specific index.

            :param index: Target index.
            :param new_point: Replacement Waypoint entity.
            :return: True if updated, False otherwise.
            :exceptions: None.
        '''
        if 0 <= index < len(self._waypoints):
            self._waypoints[index] = new_point
            return True

        return False

    def remove_point(self, index: int) -> bool:
        '''
            Removes a point at a specific index.

            :param index: Target index.
            :return: True if removed, False otherwise.
            :exceptions: None.
        '''
        if 0 <= index < len(self._waypoints):
            self._waypoints.pop(index)
            return True

        return False

    def clear(self) -> None:
        '''
            Clears all waypoints in the plan.

            :exceptions: None.
        '''
        self._waypoints.clear()

    def set_waypoints(self, waypoints: Sequence[Waypoint]) -> None:
        '''
            Replaces all waypoints with a new sequence.

            :param waypoints: Sequence of Waypoint instances.
            :exceptions: None.
        '''
        self._waypoints = list(waypoints)
