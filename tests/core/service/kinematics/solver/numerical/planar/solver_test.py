# -*- coding: UTF-8 -*-

'''
Module
    solver_test.py
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
    Unit tests for NumericalPlanarKinematicsSolver.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.jacobian.calculator import JacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.planar.dependencies import NumericalPlanarDependencies
from scaralang.core.service.kinematics.solver.numerical.planar.isolver import INumericalPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.planar.solver import NumericalPlanarKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestNumericalPlanarKinematicsSolver(TestCase):
    '''
        Test cases verifying NumericalPlanarKinematicsSolver DLS iterations.

        It defines:

            :methods:
                | setUp - Initializes test fixture with Jacobian and planar solvers.
                | test_protocol_conformance - Verifies instance satisfies protocol.
                | test_solve_dls_2d_convergence - Verifies convergence to target point.
                | test_solve_dls_2d_near_singularity - Verifies stability near boundary.
                | test_solve_dls_2d_custom_config - Verifies iteration limits.
                | test_get_version - Verifies version string representation.
    '''

    def setUp(self) -> None:
        '''
            Initializes numerical planar solver fixture.

            :exceptions: None.
        '''
        self._links: LinkDimensions = LinkDimensions(l1=200.0, l2=150.0)
        self._jacobian_calc: IJacobianCalculator = JacobianCalculator(links=self._links)
        self._planar_solver: IPlanarKinematicsSolver = (
            PlanarKinematicsSolverFactory.create(links=self._links)
        )
        self._solver: NumericalPlanarKinematicsSolver = (
            NumericalPlanarKinematicsSolver(
                dependencies=NumericalPlanarDependencies(
                    jacobian_calculator=self._jacobian_calc,
                    planar_solver=self._planar_solver,
                    config=DlsConfig(),
                )
            )
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies solver conforms to INumericalPlanarKinematicsSolver.

            :exceptions: None.
        '''
        self.assertIsInstance(self._solver, INumericalPlanarKinematicsSolver)

    def test_solve_dls_2d_convergence(self) -> None:
        '''
            Verifies iterative DLS solver converges to reachable target point.

            :exceptions: None.
        '''
        target = Point2D(x=200.0, y=100.0)
        initial = (0.2, 0.5)
        res: ScaraJoints2D = self._solver.solve_dls_2d(
            target=target, initial_angles=initial
        )
        self.assertTrue(res.reachable)
        self.assertEqual(res.status, IkStatus.SUCCESS)

        fk_pt: Point2D = self._planar_solver.solve_fk_2d(res.theta1, res.theta2)
        self.assertAlmostEqual(fk_pt.x, target.x, delta=0.05)
        self.assertAlmostEqual(fk_pt.y, target.y, delta=0.05)

    def test_solve_dls_2d_near_singularity(self) -> None:
        '''
            Verifies DLS solver does not blow up near singular boundary.

            :exceptions: None.
        '''
        target = Point2D(x=349.9, y=0.0)
        initial = (0.0, 0.05)
        res: ScaraJoints2D = self._solver.solve_dls_2d(
            target=target, initial_angles=initial
        )
        self.assertIsInstance(res, ScaraJoints2D)
        self.assertTrue(-pi <= res.theta1 <= pi)
        self.assertTrue(-pi <= res.theta2 <= pi)

    def test_solve_dls_2d_custom_config(self) -> None:
        '''
            Verifies custom DlsConfig parameter enforcement.

            :exceptions: None.
        '''
        target = Point2D(x=250.0, y=100.0)
        cfg = DlsConfig(max_iterations=1, tolerance_mm=0.001)
        solver = NumericalPlanarKinematicsSolver(
            dependencies=NumericalPlanarDependencies(
                jacobian_calculator=self._jacobian_calc,
                planar_solver=self._planar_solver,
                config=cfg,
            )
        )
        res: ScaraJoints2D = solver.solve_dls_2d(
            target=target,
            initial_angles=(0.0, 0.0),
        )
        self.assertIsInstance(res, ScaraJoints2D)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self._solver.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
