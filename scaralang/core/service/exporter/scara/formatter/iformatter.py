# -*- coding: UTF-8 -*-

'''
Module
    iformatter.py
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
    Defines structural runtime-checkable protocol IScaraWaypointFormatter
    for serializing single waypoints into SCARA DSL instruction text.
'''

from __future__ import annotations

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
class IScaraWaypointFormatter(Protocol):
    '''
    Structural protocol for formatting waypoints into SCARA DSL text.

    It defines:

        :methods:
            | format_waypoint - Formats waypoint into motion or command DSL line.
            | format_command - Formats non-motion command waypoint into DSL line.
            | get_version - Returns formatter version string.
    '''

    def format_waypoint(
        self, *, waypoint: Waypoint, is_initial: bool = False
    ) -> str:
        '''
        Formats a single trajectory waypoint into a SCARA DSL instruction line.

        :param waypoint: Trajectory Waypoint instance.
        :param is_initial: True for initial joint move, False for linear.
        :return: Formatted SCARA DSL instruction line.
        '''

    def format_command(self, *, waypoint: Waypoint) -> str:
        '''
        Formats a non-motion command waypoint into a SCARA DSL command line.

        :param waypoint: Trajectory Waypoint instance with command set.
        :return: Formatted SCARA DSL command line.
        '''

    def get_version(self) -> str:
        '''
        Returns the formatter version string representation.

        :return: Version string representation.
        '''
