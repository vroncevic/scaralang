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
    Unit tests for SpatialKinematicsSolverFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.vertical_bounds import VerticalBounds
from scaralang.core.service.kinematics.solver.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.planar.solver import PlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.spatial.factory import SpatialKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.spatial.solver import SpatialKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpatialKinematicsSolverFactory(TestCase):
    '''
        Unit tests for SpatialKinematicsSolverFactory.

        It defines:

            :methods:
                | test_create - Verifies factory create method returns protocol instance.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    def test_create(self) -> None:
        '''Verifies create returns configured SpatialKinematicsSolver.'''
        links = LinkDimensions(l1=150.0, l2=120.0)
        planar: PlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(links=links)
        vertical = VerticalBounds(z_min=-50.0, z_max=50.0)
        solver: SpatialKinematicsSolver = SpatialKinematicsSolverFactory.create(
            planar=planar, vertical=vertical
        )
        self.assertIsInstance(solver, SpatialKinematicsSolver)
        self.assertIsInstance(solver, ISpatialKinematicsSolver)

    def test_get_version(self) -> None:
        '''Verifies factory get_version returns string.'''
        version: str = SpatialKinematicsSolverFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.9')


if __name__ == '__main__':
    main()
