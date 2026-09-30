# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_read_only.py
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
    Read-only structural interface protocol for inspecting trajectory waypoints.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryReadOnly(Protocol):
    '''
        Read-only interface protocol for inspecting trajectory waypoints and count.

        It defines:

            :attributes:
                | name - Identifier name of the trajectory plan.
                | waypoints - Returns sequence of waypoints in plan.
                | count - Returns count of waypoints in plan.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the trajectory plan identifier name.

            :return: Trajectory plan name string.
        '''

    @property
    def waypoints(self) -> Sequence[Waypoint]:
        '''
            Returns immutable sequence of waypoints in plan.

            :return: Sequence of Waypoint entities.
        '''

    @property
    def count(self) -> int:
        '''
            Returns count of waypoints in plan.

            :return: Integer count.
        '''
