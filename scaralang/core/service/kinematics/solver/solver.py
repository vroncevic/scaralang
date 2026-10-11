# -*- coding: UTF-8 -*-

'''
Module
    solver.py
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
    Implementation of analytical forward and inverse SCARA kinematics calculations.
'''

from __future__ import annotations

from math import atan2, cos, pi, sin, sqrt
from typing import Final

from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsSolver:
    '''
        Analytical SCARA 2-DOF forward and inverse kinematics calculation engine.

        It defines:

            :attributes:
                | _links - Physical link dimensions of shoulder and elbow arms.
            :methods:
                | __init__ - Initializes solver with robot link dimensions.
                | solve_fk - Computes end-effector Cartesian coordinate from joint angles.
                | solve_fk_pose - Computes Cartesian positions of both elbow and tool joints.
                | solve_ik - Solves analytical inverse kinematics for joint angles.
                | get_version - Returns solver component version string.
    '''

    _links: LinkDimensions

    def __init__(self, links: LinkDimensions) -> None:
        '''
            Initializes kinematics solver with robot link dimensions.

            :param links: LinkDimensions containing arm lengths l1 and l2 in mm.
            :exceptions: None.
        '''
        self._links: Final[LinkDimensions] = links

    def solve_fk(
        self,
        theta1: float,
        theta2: float,
    ) -> Point2D:
        '''
            Computes Cartesian end-effector position from joint angles via forward kinematics.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Point2D Cartesian coordinate instance in mm.
            :exceptions: None.
        '''
        _, tool = self.solve_fk_pose(theta1, theta2)
        return tool

    def solve_fk_pose(
        self,
        theta1: float,
        theta2: float,
    ) -> tuple[Point2D, Point2D]:
        '''
            Computes Cartesian coordinates of both elbow joint and end-effector tool.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Tuple of (elbow_point, tool_point) Point2D coordinate instances in mm.
            :exceptions: None.
        '''
        l1: float = self._links.l1
        l2: float = self._links.l2
        elbow_x: float = l1 * cos(theta1)
        elbow_y: float = l1 * sin(theta1)
        total_angle: float = theta1 + theta2
        tool_x: float = elbow_x + l2 * cos(total_angle)
        tool_y: float = elbow_y + l2 * sin(total_angle)
        return Point2D(x=elbow_x, y=elbow_y), Point2D(x=tool_x, y=tool_y)

    def solve_ik(
        self,
        point: Point2D,
        elbow_left: bool = False,
    ) -> tuple[float, float] | None:
        '''
            Solves analytical inverse kinematics for SCARA 2-DOF arm.

            :param point: Target planar Cartesian coordinate point in mm.
            :param elbow_left: True for elbow-left configuration, False for elbow-right.
            :return: Tuple of (theta1, theta2) in radians, or None if unreachable.
            :exceptions: None.
        '''
        x: float = point.x
        y: float = point.y
        l1: float = self._links.l1
        l2: float = self._links.l2
        r_sq: float = x * x + y * y
        cos_theta2: float = (r_sq - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)

        if cos_theta2 < -1.0 or cos_theta2 > 1.0:
            return None

        sin_theta2: float = sqrt(max(0.0, 1.0 - cos_theta2 * cos_theta2))
        theta2: float = (
            -atan2(sin_theta2, cos_theta2)
            if elbow_left
            else atan2(sin_theta2, cos_theta2)
        )
        k1: float = l1 + l2 * cos(theta2)
        k2: float = l2 * sin(theta2)
        theta1: float = atan2(y, x) - atan2(k2, k1)

        while theta1 > pi:
            theta1 -= 2.0 * pi
        while theta1 < -pi:
            theta1 += 2.0 * pi

        return (theta1, theta2)

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
