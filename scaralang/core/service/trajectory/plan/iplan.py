# -*- coding: UTF-8 -*-

'''
Module
    iplan.py
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
    Composite structural interface protocol for complete trajectory plan domain service.
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
class ITrajectoryPlan(Protocol):
    '''
        Structural interface protocol for complete trajectory plan domain service.

        It defines:

            :attributes:
                | name - Identifier name of the trajectory plan.
                | waypoints - Returns sequence of waypoints in plan.
                | count - Returns count of waypoints in plan.
            :methods:
                | get_version - Gets implementation version string.
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
            Returns sequence of waypoints in plan.

            :return: Sequence of Waypoint entities.
        '''

    @property
    def count(self) -> int:
        '''
            Returns count of waypoints in plan.

            :return: Integer count.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string representation.
        '''
