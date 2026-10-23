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
    Unit tests for ReconfigurationFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.reconfiguration.dependencies import ReconfigurationDependencies
from scaralang.core.service.trajectory.reconfiguration.factory import ReconfigurationFactory
from scaralang.core.service.trajectory.reconfiguration.ireconfiguration_planner import IElbowReconfigurationPlanner
from scaralang.core.service.trajectory.reconfiguration.provides import ReconfigurationProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReconfigurationFactory(TestCase):
    '''
        Test cases for ReconfigurationFactory component creation and versioning.

        It defines:

            :methods:
                | test_create - Verifies factory builds a valid ReconfigurationProvides bundle.
                | test_get_version - Verifies component version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory builds a valid ReconfigurationProvides bundle.

            :exceptions: None.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dls_config: DlsConfig = DefaultScaraProfile.create_dls_config()
        kinematics = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=dls_config,
            )
        )
        deps = ReconfigurationDependencies(
            planar=kinematics.planar,
            workspace=kinematics.workspace,
        )
        provides: ReconfigurationProvides = ReconfigurationFactory.create(
            dependencies=deps
        )
        self.assertIsInstance(provides, ReconfigurationProvides)
        self.assertIsInstance(provides.planner, IElbowReconfigurationPlanner)

    def test_get_version(self) -> None:
        '''
            Verifies component version string retrieval.

            :exceptions: None.
        '''
        version = ReconfigurationFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
