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
    Defines structural protocol INumericalPlanarKinematicsSolver for iterative DLS planar IK.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class INumericalPlanarKinematicsSolver(Protocol):
    '''
        Structural protocol defining Damped Least Squares numerical planar inverse kinematics.

        It defines:

            :methods:
                | solve_dls_2d - Computes 2D joint angles via iterative DLS algorithm.
                | get_version - Returns solver component version string.
    '''

    def solve_dls_2d(
        self,
        target: Point2D,
        initial_angles: tuple[float, float],
    ) -> ScaraJoints2D:
        '''
            Solves 2D inverse kinematics using Damped Least Squares (DLS) iteration.

            :param target: Target Cartesian coordinate point in mm.
            :param initial_angles: Initial joint angles guess (theta1, theta2) in radians.
            :return: ScaraJoints2D result containing joint angles, reachability and status.
        '''

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
        '''
