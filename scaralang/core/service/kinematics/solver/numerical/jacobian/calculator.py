# -*- coding: UTF-8 -*-

'''
Module
    calculator.py
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
    Implementation of Jacobian matrix and DLS differential inverse calculator.
'''

from __future__ import annotations

from math import cos, sin
from typing import Final

from scaralang.core.model.kinematics.solver.jacobian import JacobianMatrix2D
from scaralang.core.model.kinematics.profile.link import LinkDimensions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JacobianCalculator:
    '''
        Calculates planar SCARA Jacobian matrices, DLS pseudoinverse, and manipulability.

        It defines:

            :attributes:
                | _links - Arm physical link dimensions.
            :methods:
                | __init__ - Initializes calculator with arm link dimensions.
                | compute_jacobian - Computes 2x2 forward kinematics Jacobian matrix.
                | compute_damped_inverse - Computes Damped Least Squares (DLS) pseudoinverse.
                | compute_manipulability - Calculates Yoshikawa manipulability index.
                | multiply_vector - Multiplies a 2x2 Jacobian matrix by a 2D column vector.
                | get_version - Returns calculator component version string.
    '''

    _links: LinkDimensions

    def __init__(self, links: LinkDimensions) -> None:
        '''
            Initializes Jacobian calculator with arm link dimensions.

            :param links: LinkDimensions containing l1 and l2 in mm.
            :exceptions: None.
        '''
        self._links: Final[LinkDimensions] = links

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
            :exceptions: None.
        '''
        l1: float = self._links.l1
        l2: float = self._links.l2
        s12: float = sin(theta1 + theta2)
        c12: float = cos(theta1 + theta2)

        return JacobianMatrix2D(
            j11=-l1 * sin(theta1) - l2 * s12,
            j12=-l2 * s12,
            j21=l1 * cos(theta1) + l2 * c12,
            j22=l2 * c12,
        )

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
            :exceptions: None.
        '''
        j: JacobianMatrix2D = self.compute_jacobian(theta1=theta1, theta2=theta2)
        m11: float = j.j11 * j.j11 + j.j12 * j.j12
        m12: float = j.j11 * j.j21 + j.j12 * j.j22
        m22: float = j.j21 * j.j21 + j.j22 * j.j22

        damp_sq: float = damping * damping
        a11: float = m11 + damp_sq
        a22: float = m22 + damp_sq

        inv_det: float = 1.0 / (a11 * a22 - m12 * m12)
        w11: float = a22 * inv_det
        w12: float = -m12 * inv_det
        w22: float = a11 * inv_det

        return JacobianMatrix2D(
            j11=j.j11 * w11 + j.j21 * w12,
            j12=j.j11 * w12 + j.j21 * w22,
            j21=j.j12 * w11 + j.j22 * w12,
            j22=j.j12 * w12 + j.j22 * w22,
        )

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
            :exceptions: None.
        '''
        del theta1
        return self._links.l1 * self._links.l2 * abs(sin(theta2))

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
            :exceptions: None.
        '''
        return (
            matrix.j11 * dx + matrix.j12 * dy,
            matrix.j21 * dx + matrix.j22 * dy,
        )

    def get_version(self) -> str:
        '''
            Returns calculator component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
