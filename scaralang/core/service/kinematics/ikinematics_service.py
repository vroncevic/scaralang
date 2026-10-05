# -*- coding: UTF-8 -*-

'''
Module
    ikinematics_service.py
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
    Interface protocol defining analytical SCARA kinematics calculations and reachability.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.point_3d import Point3D
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IKinematicsService(Protocol):
    '''
        Structural interface protocol for analytical SCARA kinematics calculations.

        It defines:

            :attributes:
                | bounds - Active robot geometry bounds and limits model.
                | r_min - Minimum annular workspace reach radius in mm.
                | r_max - Maximum annular workspace reach radius in mm.
            :methods:
                | solve_ik - Solves analytical inverse kinematics for joint angles.
                | solve_fk - Computes Cartesian coordinates from joint angles.
                | solve_fk_pose - Computes Cartesian positions of both elbow and tool joints.
                | is_in_workspace - Checks whether coordinates fall within annular envelope.
                | is_joint_reachable - Evaluates if position is reachable within joint limits.
    '''

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns the active robot geometry and limits model.

            :return: ScaraBounds instance.
        '''

    @property
    def r_min(self) -> float:
        '''
            Returns the minimum annular workspace reach radius in mm.

            :return: Minimum reach radius float value.
        '''

    @property
    def r_max(self) -> float:
        '''
            Returns the maximum annular workspace reach radius in mm.

            :return: Maximum reach radius float value.
        '''

    def solve_ik(
        self,
        point: Point2D,
        elbow_left: bool = False
    ) -> tuple[float, float] | None:
        '''
            Solves analytical inverse kinematics for SCARA 2-DOF arm.

            :param point: Target planar Cartesian coordinate point in mm.
            :param elbow_left: True for elbow-left configuration, False for elbow-right.
            :return: Tuple of (theta1, theta2) in radians, or None if mathematically unreachable.
        '''

    def solve_fk(
        self,
        theta1: float,
        theta2: float
    ) -> Point2D:
        '''
            Computes Cartesian end-effector position from joint angles via forward kinematics.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Point2D Cartesian coordinate instance in mm.
        '''

    def solve_fk_pose(
        self,
        theta1: float,
        theta2: float
    ) -> tuple[Point2D, Point2D]:
        '''
            Computes Cartesian coordinates of both elbow joint and end-effector tool.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Tuple of (elbow_point, tool_point) Point2D coordinate instances in mm.
        '''

    def is_in_workspace(
        self,
        point: Point3D
    ) -> tuple[bool, str]:
        '''
            Checks whether coordinates lie within the physical annular workspace and Z limits.

            :param point: Target Cartesian 3D spatial coordinate in mm.
            :return: Tuple of (is_in_bounds, error_or_warning_message).
        '''

    def is_joint_reachable(
        self,
        point: Point2D
    ) -> tuple[bool, list[str]]:
        '''
            Evaluates if target position can be achieved within physical joint limits.

            :param point: Target Cartesian 2D planar coordinate in mm.
            :return: Tuple of (is_reachable, list_of_warning_messages).
        '''
