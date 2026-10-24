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
    Implementation of spatial 4-DOF SCARA forward and inverse pose kinematics.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpatialPoseKinematicsSolver:
    '''
        Defines class SpatialPoseKinematicsSolver implementing ISpatialPoseKinematicsSolver contract.
        Analytical SCARA 4-DOF forward and inverse kinematics calculation engine.

        It defines:

            :attributes:
                | _DEFAULT_ANGLE - Default fallback joint angle in radians.
                | _planar - Injected planar 2D arm kinematics solver collaborator.
                | _vertical - Injected vertical limits for linear travel validation.
            :methods:
                | __init__ - Initializes spatial pose solver with planar solver and vertical limits.
                | solve_fk_4d - Computes 4-DOF Cartesian pose from joint coordinates.
                | solve_ik_4d - Solves 4-DOF inverse kinematics from Cartesian pose.
                | get_version - Returns solver component version string.
    '''

    _DEFAULT_ANGLE: ClassVar[float] = 0.0

    _planar: IPlanarKinematicsSolver
    _vertical: VerticalBounds

    def __init__(
        self,
        planar: IPlanarKinematicsSolver,
        vertical: VerticalBounds,
    ) -> None:
        '''
            Initializes spatial pose kinematics solver with planar solver and vertical bounds.

            :param planar: Injected IPlanarKinematicsSolver collaborator instance.
            :param vertical: Injected VerticalBounds containing z_min and z_max in mm.
            :exceptions: None.
        '''
        self._planar: Final[IPlanarKinematicsSolver] = planar
        self._vertical: Final[VerticalBounds] = vertical

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
            :exceptions: None.
        '''
        tool: Point2D = self._planar.solve_fk_2d(theta1=theta1, theta2=theta2)

        return CartesianPose(x=tool.x, y=tool.y, z=z, phi=theta4)

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
            :exceptions: None.
        '''
        if not self._vertical.z_min <= pose.z <= self._vertical.z_max:
            return ScaraJoints(
                theta1=self._DEFAULT_ANGLE,
                theta2=self._DEFAULT_ANGLE,
                z=pose.z,
                theta4=pose.phi,
                reachable=False,
                status=IkStatus.Z_LIMIT_EXCEEDED,
            )

        planar_sol: ScaraJoints2D = self._planar.solve_ik_2d(
            point=Point2D(x=pose.x, y=pose.y),
            elbow_left=elbow_left,
        )

        if not planar_sol.reachable:
            return ScaraJoints(
                theta1=planar_sol.theta1,
                theta2=planar_sol.theta2,
                z=pose.z,
                theta4=pose.phi,
                reachable=False,
                status=planar_sol.status,
            )

        return ScaraJoints(
            theta1=planar_sol.theta1,
            theta2=planar_sol.theta2,
            z=pose.z,
            theta4=pose.phi,
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
