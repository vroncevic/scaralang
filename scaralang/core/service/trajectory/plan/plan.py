# -*- coding: UTF-8 -*-

'''
Module
    plan.py
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

from scaralang.core.model.trajectory.plan.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPlan:
    '''
        TrajectoryPlan implementation holding compiled waypoints.

        It defines:

            :attributes:
                | name - Identifier name of the trajectory plan.
                | _waypoints - Immutable tuple of compiled Waypoint entities.
            :methods:
                | __init__ - Initializes trajectory plan with waypoints sequence.
                | waypoints - Returns read-only view of waypoints.
                | count - Returns total number of points in plan.
                | get_version - Gets implementation version string.
    '''

    _waypoints: tuple[Waypoint, ...]

    def __init__(self, waypoints: Sequence[Waypoint]) -> None:
        '''
            Initializes trajectory plan with waypoints sequence.

            :param waypoints: Sequence of Waypoint entities.
            :exceptions: None.
        '''
        self._waypoints = tuple(waypoints)

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
        return self._waypoints

    @property
    def count(self) -> int:
        '''
            Returns total number of points in plan.

            :return: Number of waypoints.
            :exceptions: None.
        '''
        return len(self._waypoints)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
