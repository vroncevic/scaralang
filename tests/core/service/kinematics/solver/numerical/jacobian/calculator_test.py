# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for JacobianCalculator implementation.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.jacobian import JacobianMatrix2D
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.service.kinematics.solver.numerical.jacobian.calculator import JacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJacobianCalculator(TestCase):
    '''
        Test cases verifying JacobianCalculator mathematical computations.

        It defines:

            :methods:
                | setUp - Initializes calculator with test link dimensions.
                | test_protocol_conformance - Verifies instance conforms to IJacobianCalculator.
                | test_compute_jacobian - Verifies Jacobian computation at known angles.
                | test_compute_damped_inverse - Verifies damped inverse behavior.
                | test_compute_manipulability - Verifies manipulability index computation.
                | test_multiply_vector - Verifies matrix vector multiplication.
                | test_get_version - Verifies version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with standard SCARA link lengths.

            :exceptions: None.
        '''
        self._links: LinkDimensions = LinkDimensions(l1=200.0, l2=150.0)
        self._calc: JacobianCalculator = JacobianCalculator(links=self._links)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies calculator structurally implements IJacobianCalculator.

            :exceptions: None.
        '''
        self.assertIsInstance(self._calc, IJacobianCalculator)

    def test_compute_jacobian(self) -> None:
        '''
            Verifies Jacobian elements at theta1=0, theta2=pi/2.

            :exceptions: None.
        '''
        j: JacobianMatrix2D = self._calc.compute_jacobian(theta1=0.0, theta2=pi / 2.0)
        self.assertAlmostEqual(j.j11, -150.0, places=4)
        self.assertAlmostEqual(j.j12, -150.0, places=4)
        self.assertAlmostEqual(j.j21, 200.0, places=4)
        self.assertAlmostEqual(j.j22, 0.0, places=4)

    def test_compute_damped_inverse(self) -> None:
        '''
            Verifies damped pseudoinverse calculation near singularity.

            :exceptions: None.
        '''
        inv_j: JacobianMatrix2D = self._calc.compute_damped_inverse(
            theta1=0.0, theta2=0.0, damping=0.1
        )
        self.assertIsInstance(inv_j, JacobianMatrix2D)
        self.assertTrue(abs(inv_j.j11) < 100.0)
        self.assertTrue(abs(inv_j.j22) < 100.0)

    def test_compute_manipulability(self) -> None:
        '''
            Verifies manipulability measure calculation.

            :exceptions: None.
        '''
        w_sing: float = self._calc.compute_manipulability(theta1=0.0, theta2=0.0)
        self.assertAlmostEqual(w_sing, 0.0, places=4)

        w_opt: float = self._calc.compute_manipulability(theta1=0.0, theta2=pi / 2.0)
        self.assertAlmostEqual(w_opt, 30000.0, places=4)

    def test_multiply_vector(self) -> None:
        '''
            Verifies matrix vector multiplication.

            :exceptions: None.
        '''
        mat = JacobianMatrix2D(j11=1.0, j12=2.0, j21=3.0, j22=4.0)
        res_x, res_y = self._calc.multiply_vector(mat, 2.0, 3.0)
        self.assertAlmostEqual(res_x, 8.0, places=4)
        self.assertAlmostEqual(res_y, 18.0, places=4)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self._calc.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
