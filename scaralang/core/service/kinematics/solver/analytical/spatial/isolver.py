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
    Defines structural protocol ISpatialKinematicsSolver for 3D and 4-DOF SCARA calculations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.kinematics.solver.solution_3d import ScaraJoints3D
from scaralang.core.model.kinematics.solver.solution import ScaraJoints

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISpatialKinematicsSolver(Protocol):
    '''
        Structural protocol defining spatial 3D and 4-DOF forward and inverse kinematics.

        It defines:

            :methods:
                | solve_fk_3d - Computes 3D Cartesian position from joint angles and Z height.
                | solve_ik_3d - Solves analytical inverse kinematics for 3D coordinate point.
                | solve_fk_4d - Computes 4-DOF Cartesian pose from joint coordinates.
                | solve_ik_4d - Solves 4-DOF inverse kinematics from Cartesian pose.
                | get_version - Returns solver component version string.
    '''

    def solve_fk_3d(
        self,
        theta1: float,
        theta2: float,
        z: float,
    ) -> Point3D:
        '''
            Computes 3D Cartesian position from joint angles and Z height via forward kinematics.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :param z: Linear vertical position in mm.
            :return: Point3D Cartesian coordinate instance in mm.
        '''

    def solve_ik_3d(
        self,
        point: Point3D,
        elbow_left: bool = False,
    ) -> ScaraJoints3D:
        '''
            Solves analytical inverse kinematics for 3D coordinate point with vertical limit check.

            :param point: Target Point3D Cartesian coordinate in mm.
            :param elbow_left: True for elbow-left configuration, False for right.
            :return: ScaraJoints3D instance containing joint coordinates, reachability and status.
        '''

    def solve_fk_4d(
        self,
        theta1: float,
        theta2: float,
        z: float,
        theta4: float,
    ) -> CartesianPose:
        '''
            Computes 4-DOF Cartesian pose from joint coordinates via forward kinematics.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :param z: Linear vertical position in mm.
            :param theta4: Joint 4 (wrist) angle in radians.
            :return: CartesianPose instance in mm and radians.
        '''

    def solve_ik_4d(
        self,
        pose: CartesianPose,
        elbow_left: bool = False,
    ) -> ScaraJoints:
        '''
            Solves analytical inverse kinematics for 4-DOF Cartesian pose with vertical limit check.

            :param pose: Target CartesianPose instance in mm and radians.
            :param elbow_left: True for elbow-left configuration, False for right.
            :return: ScaraJoints instance containing joint configuration, reachability and status.
        '''

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
        '''
