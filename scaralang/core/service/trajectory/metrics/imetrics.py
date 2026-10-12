# -*- coding: UTF-8 -*-

'''
Module
    imetrics.py
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
    Defines structural interface protocol for trajectory metrics calculation.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryMetrics(Protocol):
    '''
        Structural interface protocol for trajectory geometric and timing metrics calculation.

        It defines:

            :methods:
                | distance_between - Computes 3D Euclidean distance between two waypoints.
                | radial_distance - Calculates planar radial distance from robot base.
                | calculate_distance - Computes total 3D Cartesian distance along the path.
                | calculate_duration - Computes estimated execution duration based on speeds.
    '''

    def distance_between(self, p1: Waypoint, p2: Waypoint) -> float:
        '''
            Computes 3D Euclidean distance between two waypoints.

            :param p1: Source waypoint.
            :param p2: Destination waypoint.
            :return: 3D distance in mm.
        '''

    def radial_distance(self, point: Waypoint) -> float:
        '''
            Calculates planar radial distance from robot base.

            :param point: Target waypoint.
            :return: Radial distance in mm.
        '''

    def calculate_distance(self, waypoints: Sequence[Waypoint]) -> float:
        '''
            Computes total 3D Cartesian distance along the path in mm.

            :param waypoints: Sequence of waypoints.
            :return: Cumulative distance in mm.
        '''

    def calculate_duration(self, waypoints: Sequence[Waypoint]) -> float:
        '''
            Computes estimated execution duration based on waypoint speeds in seconds.

            :param waypoints: Sequence of waypoints.
            :return: Estimated duration in seconds.
        '''
