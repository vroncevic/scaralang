# -*- coding: UTF-8 -*-

'''
Module
    ispatial_checker.py
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
    Defines structural protocol ISpatialCollisionChecker for composite obstacle collision detection.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISpatialCollisionChecker(Protocol):
    '''
        Structural protocol defining composite spatial collision checking against obstacle zones.

        It defines:

            :methods:
                | is_point_colliding - Identifies obstacle zones containing a point.
                | is_segment_colliding - Identifies obstacle zones intersected by a motion segment.
                | get_version - Gets implementation version string.
    '''

    def is_point_colliding(
        self,
        *,
        point: Point2D,
        zones: tuple[ObstacleZone, ...],
    ) -> tuple[ObstacleZone, ...]:
        '''
            Identifies all obstacle zones containing a given 2D Cartesian point.

            :param point: Point2D Cartesian position.
            :param zones: Registered obstacle zones tuple.
            :return: Tuple of colliding ObstacleZone instances.
        '''

    def is_segment_colliding(
        self,
        *,
        start: Point2D,
        end: Point2D,
        zones: tuple[ObstacleZone, ...],
    ) -> tuple[ObstacleZone, ...]:
        '''
            Identifies all obstacle zones intersected by a 2D linear motion path segment.

            :param start: Starting Cartesian coordinate of motion path segment.
            :param end: Ending Cartesian coordinate of motion path segment.
            :param zones: Registered obstacle zones tuple.
            :return: Tuple of colliding ObstacleZone instances.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
