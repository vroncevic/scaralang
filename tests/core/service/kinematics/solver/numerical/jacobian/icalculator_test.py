# -*- coding: UTF-8 -*-

'''
Module
    icalculator_test.py
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
    Unit tests for IJacobianCalculator structural protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.jacobian import JacobianMatrix2D
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyJacobianCalculator:
    '''
        Dummy class implementing IJacobianCalculator protocol structurally.

        It defines:

            :methods:
                | compute_jacobian - Computes mock Jacobian matrix.
                | compute_damped_inverse - Computes mock damped inverse matrix.
                | compute_manipulability - Computes mock manipulability index.
                | multiply_vector - Computes mock vector multiplication.
                | get_version - Returns mock version string.
    '''

    def compute_jacobian(
        self,
        theta1: float,
        theta2: float,
    ) -> JacobianMatrix2D:
        '''
            Mock compute_jacobian implementation.

            :param theta1: Angle 1.
            :param theta2: Angle 2.
            :return: JacobianMatrix2D instance.
            :exceptions: None.
        '''
        del theta1, theta2
        return JacobianMatrix2D(j11=0.0, j12=0.0, j21=0.0, j22=0.0)

    def compute_damped_inverse(
        self,
        theta1: float,
        theta2: float,
        damping: float,
    ) -> JacobianMatrix2D:
        '''
            Mock compute_damped_inverse implementation.

            :param theta1: Angle 1.
            :param theta2: Angle 2.
            :param damping: Damping factor.
            :return: JacobianMatrix2D instance.
            :exceptions: None.
        '''
        del theta1, theta2, damping
        return JacobianMatrix2D(j11=0.0, j12=0.0, j21=0.0, j22=0.0)

    def compute_manipulability(
        self,
        theta1: float,
        theta2: float,
    ) -> float:
        '''
            Mock compute_manipulability implementation.

            :param theta1: Angle 1.
            :param theta2: Angle 2.
            :return: Float measure.
            :exceptions: None.
        '''
        del theta1, theta2
        return 0.0

    def multiply_vector(
        self,
        matrix: JacobianMatrix2D,
        dx: float,
        dy: float,
    ) -> tuple[float, float]:
        '''
            Mock multiply_vector implementation.

            :param matrix: JacobianMatrix2D instance.
            :param dx: Delta x.
            :param dy: Delta y.
            :return: Tuple of floats.
            :exceptions: None.
        '''
        del matrix, dx, dy
        return (0.0, 0.0)

    def get_version(self) -> str:
        '''
            Mock get_version implementation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.1.1'


class TestIJacobianCalculator(TestCase):
    '''
        Test cases verifying IJacobianCalculator structural protocol.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class conforms to protocol.
                | test_non_conforming_class - Verifies non-conforming object fails check.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IJacobianCalculator.

            :exceptions: None.
        '''
        calculator = DummyJacobianCalculator()
        self.assertIsInstance(calculator, IJacobianCalculator)

    def test_non_conforming_class(self) -> None:
        '''
            Verifies that non-conforming object fails protocol check.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), IJacobianCalculator)


if __name__ == '__main__':
    main()
