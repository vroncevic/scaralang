# -*- coding: UTF-8 -*-

'''
Module
    icalculator.py
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
    Defines structural protocol IJacobianCalculator for planar arm differential kinematics.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.solver.jacobian import JacobianMatrix2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IJacobianCalculator(Protocol):
    '''
        Structural protocol defining differential kinematics and Jacobian calculations.

        It defines:

            :methods:
                | compute_jacobian - Computes 2x2 forward kinematics Jacobian matrix.
                | compute_damped_inverse - Computes Damped Least Squares (DLS) pseudoinverse.
                | compute_manipulability - Calculates Yoshikawa manipulability dexterity index.
                | multiply_vector - Multiplies a 2x2 Jacobian matrix by a 2D column vector.
                | get_version - Returns calculator component version string.
    '''

    def compute_jacobian(
        self,
        theta1: float,
        theta2: float,
    ) -> JacobianMatrix2D:
        '''
            Computes 2x2 planar Jacobian matrix J from joint angles.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: JacobianMatrix2D instance.
        '''

    def compute_damped_inverse(
        self,
        theta1: float,
        theta2: float,
        damping: float,
    ) -> JacobianMatrix2D:
        '''
            Computes Damped Least Squares (DLS) pseudoinverse matrix J* = J^T (J J^T + lambda^2 I)^-1.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :param damping: Levenberg-Marquardt damping factor lambda.
            :return: Damped inverse JacobianMatrix2D mapping dx -> dtheta.
        '''

    def compute_manipulability(
        self,
        theta1: float,
        theta2: float,
    ) -> float:
        '''
            Calculates the scalar Yoshikawa manipulability index w = sqrt(det(J J^T)).

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Scalar manipulability measure in mm^2.
        '''

    def multiply_vector(
        self,
        matrix: JacobianMatrix2D,
        dx: float,
        dy: float,
    ) -> tuple[float, float]:
        '''
            Multiplies a 2x2 Jacobian matrix by a 2D column vector [dx, dy]^T.

            :param matrix: JacobianMatrix2D instance.
            :param dx: First component of vector.
            :param dy: Second component of vector.
            :return: Resulting 2D tuple (res_x, res_y).
        '''

    def get_version(self) -> str:
        '''
            Returns calculator component version string representation.

            :return: Semantic version string.
        '''
