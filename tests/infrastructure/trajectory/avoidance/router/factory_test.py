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
    Unit tests for DefaultRouterFactory infrastructure factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.avoidance.router.irouter import ISafeTrajectoryRouter
from scaralang.core.service.trajectory.avoidance.router.provides import RouterProvides
from scaralang.infrastructure.trajectory.avoidance.router.dependencies import DefaultRouterDependencies
from scaralang.infrastructure.trajectory.avoidance.router.factory import DefaultRouterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultRouterFactory(TestCase):
    '''
        Test cases for DefaultRouterFactory composition logic.

        It defines:

            :methods:
                | test_create - Verifies factory builds RouterProvides with configured router.
                | test_get_version - Verifies factory version string representation.
    '''

    def test_create(self) -> None:
        '''Verifies factory builds RouterProvides from default router dependencies.'''
        robot_bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        inbound_bundle = DefaultRouterDependencies(bounds=robot_bounds)
        outbound_provides: RouterProvides = DefaultRouterFactory.create(
            dependencies=inbound_bundle
        )
        self.assertIsInstance(outbound_provides, RouterProvides)
        self.assertIsInstance(outbound_provides.router, ISafeTrajectoryRouter)

    def test_get_version(self) -> None:
        '''Verifies router factory version getter.'''
        factory_version: str = DefaultRouterFactory.get_version()
        self.assertIsInstance(factory_version, str)
        self.assertTrue(len(factory_version) > 0)


if __name__ == '__main__':
    main()
