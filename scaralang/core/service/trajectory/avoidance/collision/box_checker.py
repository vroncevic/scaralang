# -*- coding: UTF-8 -*-

'''
Module
    box_checker.py
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
    Implementation of rectangular obstacle box collision detector using Liang-Barsky clipping.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BoxCollisionChecker:
    '''
        Collision checker detecting line segment intersections against rectangular obstacle boxes.

        It defines:

            :methods:
                | __init__ - Initializes BoxCollisionChecker instance.
                | is_point_inside - Checks if a point lies within box boundaries.
                | is_segment_colliding - Checks if a line segment intersects or enters box.
                | get_version - Gets implementation version string.
    '''

    def __init__(self) -> None:
        '''Initializes BoxCollisionChecker instance.'''

    def is_point_inside(
        self,
        *,
        point: Point2D,
        box: BoxObstacle,
    ) -> bool:
        '''
            Checks if a 2D Cartesian point is inside the rectangular boundary.

            :param point: Point2D position to test.
            :param box: BoxObstacle defining boundary coordinates.
            :return: True if point is within box bounds, False otherwise.
            :exceptions: None.
        '''
        return (
            box.x_min <= point.x <= box.x_max
            and box.y_min <= point.y <= box.y_max
        )

    def is_segment_colliding(
        self,
        *,
        start: Point2D,
        end: Point2D,
        box: BoxObstacle,
    ) -> bool:
        '''
            Checks if a linear motion path segment intersects the rectangular box.

            :param start: Starting Cartesian coordinate of motion segment.
            :param end: Ending Cartesian coordinate of motion segment.
            :param box: BoxObstacle defining boundary coordinates.
            :return: True if segment intersects or is inside box, False otherwise.
            :exceptions: None.
        '''
        if self.is_point_inside(point=start, box=box) or self.is_point_inside(point=end, box=box):
            return True

        dx: float = end.x - start.x
        dy: float = end.y - start.y
        p_vals: tuple[float, float, float, float] = (-dx, dx, -dy, dy)
        q_vals: tuple[float, float, float, float] = (
            start.x - box.x_min,
            box.x_max - start.x,
            start.y - box.y_min,
            box.y_max - start.y,
        )

        t0: float = 0.0
        t1: float = 1.0

        for p, q in zip(p_vals, q_vals):
            if p == 0.0:
                if q < 0.0:
                    return False
            elif p < 0.0:
                t: float = q / p
                if t > t1:
                    return False
                if t > t0:
                    t0 = t
            else:
                t = q / p
                if t < t0:
                    return False
                if t < t1:
                    t1 = t

        return t0 <= t1

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
