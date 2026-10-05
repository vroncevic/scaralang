# -*- coding: UTF-8 -*-

'''
Module
    kinematics_service_factory_test.py
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
    Unit tests for KinematicsServiceFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsServiceFactory(TestCase):
    '''
        Test cases verifying KinematicsServiceFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies factory returns IKinematicsService instance.
                | test_create_default - Verifies default factory returns IKinematicsService instance.
                | test_get_version - Verifies factory version string is present.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory produces IKinematicsService conforming instance.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        service: IKinematicsService = KinematicsServiceFactory.create(bounds=bounds)
        self.assertIsInstance(service, IKinematicsService)

    def test_create_default(self) -> None:
        '''
            Verifies factory produces IKinematicsService instance via create_default.
        '''
        service: IKinematicsService = KinematicsServiceFactory.create_default()
        self.assertIsInstance(service, IKinematicsService)
        self.assertEqual(service.bounds.links.l1, 150.0)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is present.
        '''
        version: str = KinematicsServiceFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
