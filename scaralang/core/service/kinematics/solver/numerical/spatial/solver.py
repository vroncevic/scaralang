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
    Implementation of numerical spatial Damped Least Squares (DLS) inverse kinematics solver.
'''

from __future__ import annotations

from math import pi
from typing import ClassVar, Final

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.service.kinematics.solver.numerical.planar.isolver import INumericalPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.dependencies import NumericalSpatialDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NumericalSpatialKinematicsSolver:
    '''
        Numerical spatial 4-DOF inverse kinematics solver utilizing Damped Least Squares.

        It defines:

            :attributes:
                | _PI - Mathematical constant pi in radians.
                | _TWO_PI - Two pi full circle radians constant.
                | _planar - Injected INumericalPlanarKinematicsSolver collaborator.
            :methods:
                | __init__ - Initializes solver with numerical planar kinematics solver.
                | solve_dls_4d - Computes 4-DOF joint configuration via iterative DLS algorithm.
                | get_version - Returns solver component version string.
    '''

    _PI: ClassVar[float] = pi
    _TWO_PI: ClassVar[float] = 2.0 * pi

    _planar: INumericalPlanarKinematicsSolver

    def __init__(
        self,
        dependencies: NumericalSpatialDependencies,
    ) -> None:
        '''
            Initializes numerical spatial kinematics solver with dependencies bundle.

            :param dependencies: Required NumericalSpatialDependencies bundle.
            :exceptions: None.
        '''
        self._planar: Final[INumericalPlanarKinematicsSolver] = dependencies.numerical_planar

    def solve_dls_4d(
        self,
        target_pose: CartesianPose,
        initial_joints: ScaraJoints,
    ) -> ScaraJoints:
        '''
            Solves 4-DOF inverse kinematics using Damped Least Squares (DLS) iteration.

            :param target_pose: Target CartesianPose in mm and radians.
            :param initial_joints: Initial 4-DOF joint configuration guess.
            :return: ScaraJoints result containing joint coordinates and status.
            :exceptions: None.
        '''
        res_2d: ScaraJoints2D = self._planar.solve_dls_2d(
            target=Point2D(x=target_pose.x, y=target_pose.y),
            initial_angles=(initial_joints.theta1, initial_joints.theta2),
        )
        theta4: float = (
            target_pose.phi - (res_2d.theta1 + res_2d.theta2) + self._PI
        ) % self._TWO_PI - self._PI

        return ScaraJoints(
            theta1=res_2d.theta1,
            theta2=res_2d.theta2,
            z=target_pose.z,
            theta4=theta4,
            reachable=res_2d.reachable,
            status=res_2d.status,
        )

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
