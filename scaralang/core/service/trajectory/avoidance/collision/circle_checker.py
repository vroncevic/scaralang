# -*- coding: UTF-8 -*-

'''
Module
    circle_checker.py
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
    Implementation of circular obstacle collision detector using point-to-segment distance.
'''

from __future__ import annotations

from math import hypot

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CircleCollisionChecker:
    '''
        Collision checker detecting line segment intersections against circular obstacles.

        It defines:

            :methods:
                | __init__ - Initializes CircleCollisionChecker instance.
                | is_point_inside - Checks if a point lies within circular obstacle radius.
                | is_segment_colliding - Checks if a line segment intersects or enters circle.
                | get_version - Gets implementation version string.
    '''

    def __init__(self) -> None:
        '''Initializes CircleCollisionChecker instance.'''

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
            :exceptions: None.
        '''
        dx: float = point.x - circle.center.x
        dy: float = point.y - circle.center.y

        return hypot(dx, dy) <= circle.radius

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
            :exceptions: None.
        '''
        if self.is_point_inside(point=start, circle=circle) or self.is_point_inside(
            point=end, circle=circle
        ):
            return True

        dx: float = end.x - start.x
        dy: float = end.y - start.y
        seg_len_sq: float = dx * dx + dy * dy

        if seg_len_sq == 0.0:
            return self.is_point_inside(point=start, circle=circle)

        cx: float = circle.center.x
        cy: float = circle.center.y
        t: float = ((cx - start.x) * dx + (cy - start.y) * dy) / seg_len_sq
        t_clamped: float = max(0.0, min(1.0, t))
        closest_x: float = start.x + t_clamped * dx
        closest_y: float = start.y + t_clamped * dy

        dist: float = hypot(cx - closest_x, cy - closest_y)

        return dist <= circle.radius

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
