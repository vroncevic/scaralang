# -*- coding: UTF-8 -*-

'''
Module
    irouter.py
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
    Defines structural protocol ISafeTrajectoryRouter for dead zone avoidance routing.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.trajectory.plan.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISafeTrajectoryRouter(Protocol):
    '''
        Structural protocol defining unified trajectory routing with dead zone avoidance.

        It defines:

            :methods:
                | plan_safe_trajectory - Plans safe trajectory bypassing mechanical dead zones.
                | get_version - Returns router component version string.
    '''

    def plan_safe_trajectory(
        self,
        start_point: Waypoint,
        waypoints: Sequence[Waypoint],
    ) -> list[Waypoint]:
        '''
            Plans trajectory from start point through all waypoints with dead zone avoidance.

            :param start_point: Current physical or starting position of the manipulator.
            :param waypoints: Sequence of planned target waypoints to traverse.
            :return: Ordered list of safe waypoints with detour arcs inserted where needed.
        '''

    def get_version(self) -> str:
        '''
            Returns router component version string representation.

            :return: Semantic version string.
        '''
