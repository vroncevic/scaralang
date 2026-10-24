# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for NumericalSpatialKinematicsSolverFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.jacobian.factory import JacobianCalculatorFactory
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.planar.dependencies import NumericalPlanarDependencies
from scaralang.core.service.kinematics.solver.numerical.planar.factory import NumericalPlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.numerical.planar.isolver import INumericalPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.dependencies import NumericalSpatialDependencies
from scaralang.core.service.kinematics.solver.numerical.spatial.factory import NumericalSpatialKinematicsSolverFactory
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


class TestNumericalSpatialKinematicsSolverFactory(TestCase):
    '''
        Test cases verifying NumericalSpatialKinematicsSolverFactory.

        It defines:

            :methods:
                | test_create - Verifies factory builds configured numerical spatial solver.
                | test_get_version - Verifies factory version string representation.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory constructs working NumericalSpatialKinematicsSolver.

            :exceptions: None.
        '''
        links = LinkDimensions(l1=180.0, l2=140.0)
        jac: IJacobianCalculator = JacobianCalculatorFactory.create(links=links)
        planar: IPlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(links=links)
        num_planar_deps = NumericalPlanarDependencies(
            jacobian_calculator=jac,
            planar_solver=planar,
            config=DlsConfig(),
        )
        num_planar: INumericalPlanarKinematicsSolver = (
            NumericalPlanarKinematicsSolverFactory.create(
                dependencies=num_planar_deps,
            )
        )
        spatial_deps = NumericalSpatialDependencies(
            numerical_planar=num_planar,
        )
        solver = NumericalSpatialKinematicsSolverFactory.create(
            dependencies=spatial_deps,
        )
        self.assertIsInstance(solver, INumericalSpatialKinematicsSolver)
        self.assertIsInstance(solver, NumericalSpatialKinematicsSolver)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns version string.

            :exceptions: None.
        '''
        self.assertEqual(NumericalSpatialKinematicsSolverFactory.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
