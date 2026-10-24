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
    Unit tests for NumericalSpatialKinematicsSolver.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.jacobian.calculator import JacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.planar.dependencies import NumericalPlanarDependencies
from scaralang.core.service.kinematics.solver.numerical.planar.solver import NumericalPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.dependencies import NumericalSpatialDependencies
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.solver import NumericalSpatialKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestNumericalSpatialKinematicsSolver(TestCase):
    '''
        Test cases verifying NumericalSpatialKinematicsSolver 4-DOF solutions.

        It defines:

            :methods:
                | setUp - Initializes test fixture with numerical planar collaborator.
                | test_protocol_conformance - Verifies instance satisfies protocol.
                | test_solve_dls_4d_success - Verifies 4-DOF Cartesian pose solution.
                | test_get_version - Verifies version string representation.
    '''

    def setUp(self) -> None:
        '''
            Initializes numerical spatial solver fixture.

            :exceptions: None.
        '''
        links = LinkDimensions(l1=200.0, l2=150.0)
        jac_calc: IJacobianCalculator = JacobianCalculator(links=links)
        planar: IPlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(links=links)
        num_planar = NumericalPlanarKinematicsSolver(
            dependencies=NumericalPlanarDependencies(
                jacobian_calculator=jac_calc,
                planar_solver=planar,
                config=DlsConfig(),
            )
        )
        self._solver = NumericalSpatialKinematicsSolver(
            dependencies=NumericalSpatialDependencies(
                numerical_planar=num_planar,
            )
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies solver conforms to INumericalSpatialKinematicsSolver.

            :exceptions: None.
        '''
        self.assertIsInstance(self._solver, INumericalSpatialKinematicsSolver)

    def test_solve_dls_4d_success(self) -> None:
        '''
            Verifies 4-DOF pose is solved and z / phi coordinates match.

            :exceptions: None.
        '''
        target = CartesianPose(x=200.0, y=100.0, z=-45.0, phi=0.8)
        initial = ScaraJoints(
            theta1=0.2, theta2=0.5, z=0.0, theta4=0.0, reachable=True, status=IkStatus.SUCCESS
        )
        res: ScaraJoints = self._solver.solve_dls_4d(
            target_pose=target,
            initial_joints=initial,
        )
        self.assertTrue(res.reachable)
        self.assertEqual(res.status, IkStatus.SUCCESS)
        self.assertEqual(res.z, -45.0)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self._solver.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
