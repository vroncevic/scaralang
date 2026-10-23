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
    Implementation of planar 2D SCARA arm analytical forward and inverse kinematics.
'''

from __future__ import annotations

from math import atan2, cos, pi, sin, sqrt
from typing import ClassVar, Final

from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanarKinematicsSolver:
    '''
        Analytical SCARA 2-DOF planar forward and inverse kinematics calculation engine.

        It defines:

            :attributes:
                | _DEFAULT_ANGLE - Default fallback joint angle in radians.
                | _MAX_COS - Maximum allowed cosine value for reach checks.
                | _MIN_COS - Minimum allowed cosine value for reach checks.
                | _MIN_RADICAND - Minimum floor value for square root radicand.
                | _PI - Pi mathematical constant in radians.
                | _SCALE_TWO - Constant divisor scaling factor of two.
                | _TWO_PI - Two pi full circle radians constant.
                | _links - Physical link dimensions of shoulder and elbow arms.
            :methods:
                | __init__ - Initializes solver with robot link dimensions.
                | solve_fk_2d - Computes end-effector Cartesian coordinate from joint angles.
                | solve_fk_pose_2d - Computes Cartesian positions of elbow and tool joints.
                | solve_ik_2d - Solves analytical inverse kinematics for joint angles.
                | get_version - Returns solver component version string.
    '''

    _DEFAULT_ANGLE: ClassVar[float] = 0.0
    _MIN_COS: ClassVar[float] = -1.0
    _MAX_COS: ClassVar[float] = 1.0
    _MIN_RADICAND: ClassVar[float] = 0.0
    _SCALE_TWO: ClassVar[float] = 2.0
    _PI: ClassVar[float] = pi
    _TWO_PI: ClassVar[float] = 2.0 * pi

    _links: LinkDimensions

    def __init__(self, links: LinkDimensions) -> None:
        '''
            Initializes planar kinematics solver with robot link dimensions.

            :param links: LinkDimensions containing arm lengths l1 and l2 in mm.
            :exceptions: None.
        '''
        self._links: Final[LinkDimensions] = links

    def solve_fk_2d(
        self,
        theta1: float,
        theta2: float,
    ) -> Point2D:
        '''
            Computes Cartesian end-effector position from joint angles via 2D forward kinematics.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Point2D Cartesian coordinate instance in mm.
            :exceptions: None.
        '''
        x: float = (
            self._links.l1 * cos(theta1)
            + self._links.l2 * cos(theta1 + theta2)
        )
        y: float = (
            self._links.l1 * sin(theta1)
            + self._links.l2 * sin(theta1 + theta2)
        )

        return Point2D(x=x, y=y)

    def solve_fk_pose_2d(
        self,
        theta1: float,
        theta2: float,
    ) -> tuple[Point2D, Point2D]:
        '''
            Computes Cartesian coordinates of both elbow joint and end-effector tool in 2D.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Tuple of (elbow_point, tool_point) Point2D coordinate instances in mm.
            :exceptions: None.
        '''
        elbow_x: float = self._links.l1 * cos(theta1)
        elbow_y: float = self._links.l1 * sin(theta1)
        tool_x: float = elbow_x + self._links.l2 * cos(theta1 + theta2)
        tool_y: float = elbow_y + self._links.l2 * sin(theta1 + theta2)

        return (Point2D(x=elbow_x, y=elbow_y), Point2D(x=tool_x, y=tool_y))

    def solve_ik_2d(
        self,
        point: Point2D,
        elbow_left: bool = False,
    ) -> ScaraJoints2D:
        '''
            Solves analytical inverse kinematics for SCARA 2-DOF planar arm.

            :param point: Target planar Cartesian coordinate point in mm.
            :param elbow_left: True for elbow-left configuration, False for right.
            :return: ScaraJoints2D instance containing joint angles, reachability and status.
            :exceptions: None.
        '''
        r_sq: float = point.x * point.x + point.y * point.y
        l1: float = self._links.l1
        l2: float = self._links.l2
        cos_theta2: float = (r_sq - l1 * l1 - l2 * l2) / (self._SCALE_TWO * l1 * l2)

        if cos_theta2 < self._MIN_COS:
            return ScaraJoints2D(
                theta1=self._DEFAULT_ANGLE,
                theta2=self._DEFAULT_ANGLE,
                reachable=False,
                status=IkStatus.INNER_DEADZONE,
            )

        if cos_theta2 > self._MAX_COS:
            return ScaraJoints2D(
                theta1=self._DEFAULT_ANGLE,
                theta2=self._DEFAULT_ANGLE,
                reachable=False,
                status=IkStatus.OUT_OF_REACH,
            )

        sin_theta2: float = sqrt(
            max(self._MIN_RADICAND, self._MAX_COS - cos_theta2 * cos_theta2)
        )

        if elbow_left:
            sin_theta2 = -sin_theta2

        theta2: float = atan2(sin_theta2, cos_theta2)
        k1: float = l1 + l2 * cos_theta2
        k2: float = l2 * sin_theta2
        theta1: float = atan2(point.y, point.x) - atan2(k2, k1)

        theta1 = (theta1 + self._PI) % self._TWO_PI - self._PI
        theta2 = (theta2 + self._PI) % self._TWO_PI - self._PI

        return ScaraJoints2D(
            theta1=theta1,
            theta2=theta2,
            reachable=True,
            status=IkStatus.SUCCESS,
        )

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
