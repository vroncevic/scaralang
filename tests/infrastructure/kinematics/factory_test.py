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
    Unit tests for DefaultKinematicsFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.planar.isolver import INumericalPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultKinematicsFactory(TestCase):
    '''
        Test cases verifying DefaultKinematicsFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns KinematicsProvides with default bounds.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns operational KinematicsProvides bundle.

            :exceptions: None.
        '''
        provides: KinematicsProvides = DefaultKinematicsFactory.create()
        self.assertIsInstance(provides, KinematicsProvides)
        self.assertIsInstance(provides.envelope, IWorkspaceEnvelope)
        self.assertIsInstance(provides.planar, IPlanarKinematicsSolver)
        self.assertIsInstance(provides.spatial, ISpatialKinematicsSolver)
        self.assertIsInstance(provides.workspace, IWorkspaceBoundsEvaluator)
        self.assertIsInstance(provides.jacobian, IJacobianCalculator)
        self.assertIsInstance(provides.numerical_planar, INumericalPlanarKinematicsSolver)
        self.assertIsInstance(provides.numerical_spatial, INumericalSpatialKinematicsSolver)
        self.assertEqual(provides.envelope.bounds.links.l1, 150.0)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns valid semantic version string.

            :exceptions: None.
        '''
        version: str = DefaultKinematicsFactory.get_version()
        self.assertEqual(version, '1.1.0')


if __name__ == '__main__':
    main()
