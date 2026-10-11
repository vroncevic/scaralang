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
    Unit tests for KinematicsFactory component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.iservice import IKinematicsService
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.solver.isolver import IKinematicsSolver
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsFactory(TestCase):
    '''
        Test cases verifying KinematicsFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies factory returns KinematicsProvides bundle.
                | test_get_version - Verifies factory version string is present.
    '''

    def test_create(self) -> None:
        '''Verifies factory produces KinematicsProvides containing all expected services.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dependencies = KinematicsDependencies(bounds=bounds)
        provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=dependencies
        )
        self.assertIsInstance(provides, KinematicsProvides)
        self.assertIsInstance(provides.service, IKinematicsService)
        self.assertIsInstance(provides.solver, IKinematicsSolver)
        self.assertIsInstance(provides.workspace, IWorkspaceBoundsEvaluator)
        self.assertEqual(provides.service.bounds, bounds)

    def test_get_version(self) -> None:
        '''Verifies factory version string is present.'''
        version: str = KinematicsFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
