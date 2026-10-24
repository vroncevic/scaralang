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
    Unit tests for SpatialPoseKinematicsSolverFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.solver import PlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.pose.factory import SpatialPoseKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.spatial.pose.isolver import ISpatialPoseKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.pose.solver import SpatialPoseKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpatialPoseKinematicsSolverFactory(TestCase):
    '''
        Validates SpatialPoseKinematicsSolverFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies factory builds configured SpatialPoseKinematicsSolver.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory builds configured SpatialPoseKinematicsSolver.

            :exceptions: None.
        '''
        links = LinkDimensions(l1=150.0, l2=120.0)
        planar: PlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(links=links)
        vertical = VerticalBounds(z_min=-50.0, z_max=50.0)
        solver: SpatialPoseKinematicsSolver = SpatialPoseKinematicsSolverFactory.create(
            planar=planar, vertical=vertical
        )
        self.assertIsInstance(solver, SpatialPoseKinematicsSolver)
        self.assertTrue(isinstance(solver, ISpatialPoseKinematicsSolver))

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(SpatialPoseKinematicsSolverFactory.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
