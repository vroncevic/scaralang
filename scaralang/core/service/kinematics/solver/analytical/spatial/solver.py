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
    Implementation of spatial 3D and 4-DOF SCARA forward and inverse kinematics.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.model.kinematics.solver.solution_3d import ScaraJoints3D
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.pose.isolver import ISpatialPoseKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpatialKinematicsSolver:
    '''
        Analytical SCARA spatial 3D and 4-DOF forward and inverse kinematics calculation engine.

        It defines:

            :attributes:
                | _DEFAULT_ANGLE - Default fallback joint angle in radians.
                | _planar - Injected planar 2D arm kinematics solver collaborator.
                | _vertical - Injected vertical limits for linear travel validation.
                | _pose_solver - Injected 4-DOF orientation pose kinematics collaborator.
            :methods:
                | __init__ - Initializes spatial solver with planar, vertical and pose solvers.
                | solve_fk_3d - Computes 3D Cartesian position from joint angles and Z height.
                | solve_ik_3d - Solves analytical inverse kinematics for 3D coordinate point.
                | solve_fk_4d - Computes 4-DOF Cartesian pose from joint coordinates.
                | solve_ik_4d - Solves 4-DOF inverse kinematics from Cartesian pose.
                | get_version - Returns solver component version string.
    '''

    _DEFAULT_ANGLE: ClassVar[float] = 0.0

    _planar: IPlanarKinematicsSolver
    _vertical: VerticalBounds
    _pose_solver: ISpatialPoseKinematicsSolver

    def __init__(
        self,
        planar: IPlanarKinematicsSolver,
        vertical: VerticalBounds,
        pose_solver: ISpatialPoseKinematicsSolver,
    ) -> None:
        '''
            Initializes spatial kinematics solver with planar, vertical and pose solvers.

            :param planar: Injected IPlanarKinematicsSolver collaborator instance.
            :param vertical: Injected VerticalBounds containing z_min and z_max in mm.
            :param pose_solver: Injected ISpatialPoseKinematicsSolver collaborator instance.
            :exceptions: None.
        '''
        self._planar: Final[IPlanarKinematicsSolver] = planar
        self._vertical: Final[VerticalBounds] = vertical
        self._pose_solver: Final[ISpatialPoseKinematicsSolver] = pose_solver

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
            :exceptions: None.
        '''
        tool: Point2D = self._planar.solve_fk_2d(theta1=theta1, theta2=theta2)

        return Point3D(x=tool.x, y=tool.y, z=z)

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
            :exceptions: None.
        '''
        if not self._vertical.z_min <= point.z <= self._vertical.z_max:
            return ScaraJoints3D(
                theta1=self._DEFAULT_ANGLE,
                theta2=self._DEFAULT_ANGLE,
                z=point.z,
                reachable=False,
                status=IkStatus.Z_LIMIT_EXCEEDED,
            )

        planar_sol: ScaraJoints2D = self._planar.solve_ik_2d(
            point=Point2D(x=point.x, y=point.y),
            elbow_left=elbow_left,
        )

        if not planar_sol.reachable:
            return ScaraJoints3D(
                theta1=planar_sol.theta1,
                theta2=planar_sol.theta2,
                z=point.z,
                reachable=False,
                status=planar_sol.status,
            )

        return ScaraJoints3D(
            theta1=planar_sol.theta1,
            theta2=planar_sol.theta2,
            z=point.z,
            reachable=True,
            status=IkStatus.SUCCESS,
        )

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
        return self._pose_solver.solve_fk_4d(
            theta1=theta1,
            theta2=theta2,
            z=z,
            theta4=theta4,
        )

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
        return self._pose_solver.solve_ik_4d(
            pose=pose,
            elbow_left=elbow_left,
        )

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
