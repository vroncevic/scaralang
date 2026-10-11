# -*- coding: UTF-8 -*-

'''
Module
    isolver.py
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
    Defines structural protocol IKinematicsSolver for forward and inverse kinematics calculations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IKinematicsSolver(Protocol):
    '''
        Structural protocol defining forward and inverse kinematics operations.

        It defines:

            :methods:
                | solve_fk - Computes end-effector Cartesian coordinate from joint angles.
                | solve_fk_pose - Computes Cartesian positions of both elbow and tool joints.
                | solve_ik - Solves analytical inverse kinematics for joint angles.
                | get_version - Returns solver component version string.
    '''

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

    def solve_ik(
        self,
        point: Point2D,
        elbow_left: bool = False,
    ) -> tuple[float, float] | None:
        '''
            Solves analytical inverse kinematics for SCARA 2-DOF arm.

            :param point: Target planar Cartesian coordinate point in mm.
            :param elbow_left: True for elbow-left configuration, False for elbow-right.
            :return: Tuple of (theta1, theta2) in radians, or None if mathematically unreachable.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
