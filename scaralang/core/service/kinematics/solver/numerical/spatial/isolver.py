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
    Defines structural protocol INumericalSpatialKinematicsSolver for iterative DLS spatial IK.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
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
class INumericalSpatialKinematicsSolver(Protocol):
    '''
        Structural protocol defining Damped Least Squares numerical spatial inverse kinematics.

        It defines:

            :methods:
                | solve_dls_4d - Computes 4-DOF joint configuration via iterative DLS algorithm.
                | get_version - Returns solver component version string.
    '''

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
        '''

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
        '''
