# -*- coding: UTF-8 -*-

'''
Module
    icircle_checker.py
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
    Defines structural protocol ICircleCollisionChecker for circular obstacle collision tests.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICircleCollisionChecker(Protocol):
    '''
        Structural protocol defining collision detection against circular obstacles.

        It defines:

            :methods:
                | is_point_inside - Checks if a point lies within circular obstacle radius.
                | is_segment_colliding - Checks if a line segment intersects or enters circle.
                | get_version - Gets implementation version string.
    '''

    def is_point_inside(
        self,
        *,
        point: Point2D,
        circle: CircleObstacle,
    ) -> bool:
        '''
            Checks if a 2D Cartesian point is inside the circular boundary.

            :param point: Point2D position to test.
            :param circle: CircleObstacle defining center and radius.
            :return: True if point is within circle, False otherwise.
        '''

    def is_segment_colliding(
        self,
        *,
        start: Point2D,
        end: Point2D,
        circle: CircleObstacle,
    ) -> bool:
        '''
            Checks if a linear motion path segment intersects the circular obstacle.

            :param start: Starting Cartesian coordinate of motion segment.
            :param end: Ending Cartesian coordinate of motion segment.
            :param circle: CircleObstacle defining center and radius.
            :return: True if segment intersects or enters circle, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
